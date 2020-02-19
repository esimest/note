# kube-apiserver 源码分析

kube-apiserver 是一个提供了对集群资源(对象)的 CRUD 功能的 restful WebServer.
因此分析 kube-apiserver 主要分析两个方面:

1. kube-apiserver 如何启动一个 WebServer.

2. kube-apiserver 如何与后端存储交互.

kube-apiserver 中几类常见的类型命名:

- `***Options` 与命令行参数相关的类型;

- `***Config` 与服务配置相关的类型;

- `***Server` kube-apiserver 启动的 server(包含: `APIExtensionsServer` `KubeAPIServer` `AggregatorServer`);

- `***Storage` 资源对象;

## 启动流程

```go
// 启动文件 \\kubernetes\cmd\kube-apiserver\apiserver.go
func main() {
    ...
	command := app.NewAPIServerCommand()      // type(command) == *cobra.Command
    ...
	if err := command.Execute(); err != nil { // Execute() 执行该 command, 会调用 command.Run/RunE 方法(为命令的核心逻辑)
		os.Exit(1)
	}
}

// NewAPIServerCommand: \\kubernetes\cmd\kube-apiserver\app\server.go
func NewAPIServerCommand() *cobra.Command {
	s := options.NewServerRunOptions()
	cmd := &cobra.Command{
        ...
		RunE: func(cmd *cobra.Command, args []string) error {
			verflag.PrintAndExitIfRequested()  // 检查参数是否为 -version, 如果是: 打印版本并退出.
			utilflag.PrintFlags(cmd.Flags())   // 打印 flags.

			// set default options
			completedOptions, err := Complete(s) // 设置默认 options(options 解析完成后执行).
			if err != nil {
				return err
			}

			// validate options
			if errs := completedOptions.Validate(); len(errs) != 0 {
				return utilerrors.NewAggregate(errs)
			}

			return Run(completedOptions, genericapiserver.SetupSignalHandler())  // kube-apiserver 命令的核心逻辑.
		},
	}
    ... // 解析 options 和配置 Usage 函数.
	return cmd
}

// 启动 api-server 组件
// Run \\kubernetes\cmd\kube-apiserver\app\server.go
// Run runs the specified APIServer.  This should never exit.
func Run(completeOptions completedServerRunOptions, stopCh <-chan struct{}) error {
	// To help debugging, immediately log version
	klog.Infof("Version: %+v", version.Get())

    // 责任链模式(Chain of Responsibility Pattern)为请求创建了一个接收者对象的链;
    // 这种模式给予请求的类型, 对请求的发送者和接收者进行解耦;
    // 在这种模式中; 通常每个接收者都包含对另一个接收者的引用;
    // 如果一个对象不能处理该请求, 那么它会把相同的请求传给下一个接收者. 依此类推.
	server, err := CreateServerChain(completeOptions, stopCh)
	if err != nil {
		return err
	}

	prepared, err := server.PrepareRun()
	if err != nil {
		return err
	}

    // 启动 Server
	return prepared.Run(stopCh)
}

// \\kubernetes\cmd\kube-apiserver\app\server.go, 用于创建 servers
// CreateServerChain creates the apiservers connected via delegation.
func CreateServerChain(completedOptions completedServerRunOptions, stopCh <-chan struct{}) (*aggregatorapiserver.APIAggregator, error) {
	nodeTunneler, proxyTransport, err := CreateNodeDialer(completedOptions) // 忽略
	if err != nil {
		return nil, err
	}

	kubeAPIServerConfig, insecureServingInfo, serviceResolver, pluginInitializer, err := CreateKubeAPIServerConfig(completedOptions, nodeTunneler, proxyTransport)
	if err != nil {
		return nil, err
	}

	// If additional API servers are added, they should be gated.
	apiExtensionsConfig, err := createAPIExtensionsConfig(*kubeAPIServerConfig.GenericConfig, kubeAPIServerConfig.ExtraConfig.VersionedInformers, pluginInitializer, completedOptions.ServerRunOptions, completedOptions.MasterCount,
		serviceResolver, webhook.NewDefaultAuthenticationInfoResolverWrapper(proxyTransport, kubeAPIServerConfig.GenericConfig.LoopbackClientConfig))
	if err != nil {
		return nil, err
    }
    // 创建 APIExtensions Server
    // type(apiExtensionsServer) == *extensionsapiserver.CustomResourceDefinitions
	apiExtensionsServer, err := createAPIExtensionsServer(apiExtensionsConfig, genericapiserver.NewEmptyDelegate())
	if err != nil {
		return nil, err
	}

    // 创建 KubeAPI Server
    // type(kubeAPIServer) == *master.Master
	kubeAPIServer, err := CreateKubeAPIServer(kubeAPIServerConfig, apiExtensionsServer.GenericAPIServer)
	if err != nil {
		return nil, err
	}

	// aggregator comes last in the chain
	aggregatorConfig, err := createAggregatorConfig(*kubeAPIServerConfig.GenericConfig, completedOptions.ServerRunOptions, kubeAPIServerConfig.ExtraConfig.VersionedInformers, serviceResolver, proxyTransport, pluginInitializer)
	if err != nil {
		return nil, err
    }
    // 创建聚合 Server
    // GenericAPIServer: 通用 APIServer
    // type(aggregatorServer) == *aggregatorapiserver.APIAggregator
	aggregatorServer, err := createAggregatorServer(aggregatorConfig, kubeAPIServer.GenericAPIServer, apiExtensionsServer.Informers)
	if err != nil {
		// we don't need special handling for innerStopCh because the aggregator server doesn't create any go routines
		return nil, err
	}

	if insecureServingInfo != nil {
		insecureHandlerChain := kubeserver.BuildInsecureHandlerChain(aggregatorServer.GenericAPIServer.UnprotectedHandler(), kubeAPIServerConfig.GenericConfig)
		if err := insecureServingInfo.Serve(insecureHandlerChain, kubeAPIServerConfig.GenericConfig.RequestTimeout, stopCh); err != nil {
			return nil, err
		}
	}

	return aggregatorServer, nil
}

// prepared.Run 实际调用的是 preparedGenericAPIServer.Run
// \\kubernetes\staging\src\k8s.io\apiserver\pkg\server\genericapiserver.go
// Run spawns the secure http server. It only returns if stopCh is closed
// or the secure port cannot be listened on initially.
func (s preparedGenericAPIServer) Run(stopCh <-chan struct{}) error {
...
}
```

## Options(配置)

[kube-apiserver options](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/)

```go
// ServerRunOptions kube-apiserver 配置对象
// D:\GitHub\kubernetes\cmd\kube-apiserver\app\options\options.go
// ServerRunOptions runs a kubernetes api server.
type ServerRunOptions struct {
	GenericServerRunOptions *genericoptions.ServerRunOptions
	Etcd                    *genericoptions.EtcdOptions
	SecureServing           *genericoptions.SecureServingOptionsWithLoopback
	InsecureServing         *genericoptions.DeprecatedInsecureServingOptionsWithLoopback
	Audit                   *genericoptions.AuditOptions
	Features                *genericoptions.FeatureOptions
	Admission               *kubeoptions.AdmissionOptions
	Authentication          *kubeoptions.BuiltInAuthenticationOptions
	Authorization           *kubeoptions.BuiltInAuthorizationOptions
	CloudProvider           *kubeoptions.CloudProviderOptions
	APIEnablement           *genericoptions.APIEnablementOptions
	EgressSelector          *genericoptions.EgressSelectorOptions

	AllowPrivileged           bool
	EnableLogsHandler         bool
	EventTTL                  time.Duration
	KubeletConfig             kubeletclient.KubeletClientConfig
	KubernetesServiceNodePort int
	MaxConnectionBytesPerSec  int64
	// ServiceClusterIPRange is mapped to input provided by user
	ServiceClusterIPRanges string
	//PrimaryServiceClusterIPRange and SecondaryServiceClusterIPRange are the results
	// of parsing ServiceClusterIPRange into actual values
	PrimaryServiceClusterIPRange   net.IPNet
	SecondaryServiceClusterIPRange net.IPNet

	ServiceNodePortRange utilnet.PortRange
	SSHKeyfile           string
	SSHUser              string

	ProxyClientCertFile string
	ProxyClientKeyFile  string

	EnableAggregatorRouting bool

	MasterCount            int
	EndpointReconcilerType string

	ServiceAccountSigningKeyFile     string
	ServiceAccountIssuer             serviceaccount.TokenGenerator
	ServiceAccountTokenMaxExpiration time.Duration
}

// Etcd Options D:\GitHub\kubernetes\staging\src\k8s.io\apiserver\pkg\server\options\etcd.go
type EtcdOptions struct {
	// The value of Paging on StorageConfig will be overridden by the
	// calculated feature gate value.
	StorageConfig                    storagebackend.Config
	EncryptionProviderConfigFilepath string

	EtcdServersOverrides []string

	// To enable protobuf as storage format, it is enough
	// to set it to "application/vnd.kubernetes.protobuf".
	DefaultStorageMediaType string
	DeleteCollectionWorkers int
	EnableGarbageCollection bool

	// Set EnableWatchCache to false to disable all watch caches
	EnableWatchCache bool
	// Set DefaultWatchCacheSize to zero to disable watch caches for those resources that have no explicit cache size set
	DefaultWatchCacheSize int
	// WatchCacheSizes represents override to a given resource
	WatchCacheSizes []string
}

// storage D:\GitHub\kubernetes\staging\src\k8s.io\apiserver\pkg\storage\storagebackend\config.go
// Config is configuration for creating a storage backend.
type Config struct {
	// Type defines the type of storage backend. Default ("") is "etcd3".
	Type string
	// Prefix is the prefix to all keys passed to storage.Interface methods.
	Prefix string
	// Transport holds all connection related info, i.e. equal TransportConfig means equal servers we talk to.
	Transport TransportConfig
	// Paging indicates whether the server implementation should allow paging (if it is
	// supported). This is generally configured by feature gating, or by a specific
	// resource type not wishing to allow paging, and is not intended for end users to
	// set.
	Paging bool

	Codec runtime.Codec
	// EncodeVersioner is the same groupVersioner used to build the
	// storage encoder. Given a list of kinds the input object might belong
	// to, the EncodeVersioner outputs the gvk the object will be
	// converted to before persisted in etcd.
	EncodeVersioner runtime.GroupVersioner
	// Transformer allows the value to be transformed prior to persisting into etcd.
	Transformer value.Transformer

	// CompactionInterval is an interval of requesting compaction from apiserver.
	// If the value is 0, no compaction will be issued.
	CompactionInterval time.Duration
	// CountMetricPollPeriod specifies how often should count metric be updated
	CountMetricPollPeriod time.Duration
}

// TransportConfig holds all connection related info,  i.e. equal TransportConfig means equal servers we talk to.
type TransportConfig struct {
	// ServerList is the list of storage servers to connect with.
	ServerList []string
	// TLS credentials
	KeyFile       string
	CertFile      string
	TrustedCAFile string
	// function to determine the egress dialer. (i.e. konnectivity server dialer)
	EgressLookup egressselector.Lookup
}
```
