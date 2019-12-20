# Flask

## 构造方法 Flask(__name__)

Flask() 的第一个位置参数 import_name, 主要用于获取项目相关的资源，如模板资源、静态资源等。
新版本增加了 root_path 参数，当没有指定时，使用的时 __name__ 所指定的包的目录

```python
# Flask 父类的构造方法
class _PackageBoundObject(object):
    #: The name of the package or module that this app belongs to. Do not
    #: change this once it is set by the constructor.
    import_name = None

    #: Location of the template files to be added to the template lookup.
    #: ``None`` if templates should not be added.
    template_folder = None

    #: Absolute path to the package on the filesystem. Used to look up
    #: resources contained in the package.
    root_path = None

    def __init__(self, import_name, template_folder=None, root_path=None):
        self.import_name = import_name
        self.template_folder = template_folder

        if root_path is None:
            root_path = get_root_path(self.import_name)

        self.root_path = root_path
        self._static_folder = None
        self._static_url_path = None

        # circular import
        from .cli import AppGroup

        #: The Click command group for registration of CLI commands
        #: on the application and associated blueprints. These commands
        #: are accessible via the :command:`flask` command once the
        #: application has been discovered and blueprints registered.
        self.cli = AppGroup()

# get_root_path 的实现
def get_root_path(import_name):
    mod = sys.modules.get(import_name)
    if mod is not None and hasattr(mod, "__file__"):
        return os.path.dirname(os.path.abspath(mod.__file__))

    # Next attempt: check the loader.
    loader = pkgutil.get_loader(import_name)

    if loader is None or import_name == "__main__":
        return os.getcwd()

    # For .egg, zipimporter does not have get_filename until Python 2.7.
    # Some other loaders might exhibit the same behavior.
    if hasattr(loader, "get_filename"):
        filepath = loader.get_filename(import_name)
    else:
        # 此处省略了具体内容
    return os.path.dirname(os.path.abspath(filepath))
```