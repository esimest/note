# kube-apiserver 源码分析

[kube-apiserver options](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/)

## 启动流程

```go
// 启动文件 D:\GitHub\kubernetes\cmd\kube-apiserver\apiserver.go
func main() {
    ...
	command := app.NewAPIServerCommand()      // type(command) == *cobra.Command
    ...
	if err := command.Execute(); err != nil { // Execute() 执行该 command, 会调用 command.Run/RunE 方法(为命令的核心逻辑)
		os.Exit(1)
	}
}

// NewAPIServerCommand: D:\GitHub\kubernetes\cmd\kube-apiserver\app\server.go
func NewAPIServerCommand() *cobra.Command {
	s := options.NewServerRunOptions()
	cmd := &cobra.Command{
        ...
		RunE: func(cmd *cobra.Command, args []string) error {
			verflag.PrintAndExitIfRequested()  // 检查参数是否为 -version, 如果是: 打印版本并退出.
			utilflag.PrintFlags(cmd.Flags())   // 打印 flags.

			// set default options
			completedOptions, err := Complete(s) // 设置默认 options.
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
    ... // 后续为加载 flags 和配置 Usage 函数.
	return cmd
}

// Run D:\GitHub\kubernetes\cmd\kube-apiserver\app\server.go
// Run runs the specified APIServer.  This should never exit.
func Run(completeOptions completedServerRunOptions, stopCh <-chan struct{}) error {
	// To help debugging, immediately log version
	klog.Infof("Version: %+v", version.Get())

	server, err := CreateServerChain(completeOptions, stopCh)  // delegation 模式, 对象委托另外一个对象处理.
	if err != nil {
		return err
	}

	prepared, err := server.PrepareRun()
	if err != nil {
		return err
	}

	return prepared.Run(stopCh)
}

// D:\GitHub\kubernetes\cmd\kube-apiserver\app\server.go, 用于创建 servers
// CreateServerChain creates the apiservers connected via delegation.
func CreateServerChain(completedOptions completedServerRunOptions, stopCh <-chan struct{}) (*aggregatorapiserver.APIAggregator, error) {
	nodeTunneler, proxyTransport, err := CreateNodeDialer(completedOptions)
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
```