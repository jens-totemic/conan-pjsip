import os
import stat
from conans import ConanFile, AutoToolsBuildEnvironment, tools

# based on https://github.com/conan-community/conan-ncurses/blob/stable/6.1/conanfile.py
class PjsipConan(ConanFile):
    name = "pjsip"
    version = "2.8"
    license = "GPL2"
    homepage = "https://github.com/totemic/pjproject"
    description = "PJSIP is a free and open source multimedia communication library written in C language implementing standard based protocols such as SIP, SDP, RTP, STUN, TURN, and ICE."
    url = "https://github.com/jens-totemic/conan-pjsip"    
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "SSL": [True, False],
               "fPIC": [True, False]}
    # if no OpenSSL is found, pjsip might try to use GnuTLS
    default_options = {"shared": False, "SSL": True, "fPIC": True}   
    generators = "cmake"
    exports = "LICENSE"
    _autotools = None
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            del self.options.shared

    def source(self):
        tools.get("%s/archive/%s.zip" % (self.homepage, self.version))
        os.rename("pjproject-%s" % self.version, self._source_subfolder)
        if not tools.os_info.is_windows:
            configure_file = os.path.join(self._source_subfolder, "configure")
            stc = os.stat(configure_file)
            os.chmod(configure_file, stc.st_mode | stat.S_IEXEC)        
            aconfigure_file = os.path.join(self._source_subfolder, "aconfigure")
            stac = os.stat(aconfigure_file)
            os.chmod(aconfigure_file, stac.st_mode | stat.S_IEXEC)

    def requirements(self):
        if self.options.SSL:
            self.requires("OpenSSL/1.0.2@conan/stable")

    def _configure_autotools(self):
        if not self._autotools:
            args = ["--enable-shared"] if self.options.shared else None                   
            self._autotools = AutoToolsBuildEnvironment(self)
            self._autotools.configure(args=args)        
        return self._autotools
        
    def build(self):
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            #self.output.info("Variables")
            env_build_vars = autotools.vars
            # The include paths for dependencies are added to the CPPFLAGS
            # which are not used by pjsip's makefiles. Instead, add them to CFLAGS
            cflags = env_build_vars['CFLAGS'] + " " + env_build_vars['CPPFLAGS']
            env_build_vars['CFLAGS'] = cflags
            self.output.info(env_build_vars)
            autotools.make(vars=env_build_vars)

    def package(self):
#        self.copy("*.h", dst="include", src="hello")
#        self.copy("*hello.lib", dst="lib", keep_path=False)
#        self.copy("*.dll", dst="bin", keep_path=False)
#        self.copy("*.so", dst="lib", keep_path=False)
#        self.copy("*.dylib", dst="lib", keep_path=False)
#        self.copy("*.a", dst="lib", keep_path=False)

        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.exelinkflags.append("-framework CoreAudio")
        self.cpp_info.exelinkflags.append("-framework CoreServices")
        self.cpp_info.exelinkflags.append("-framework AudioUnit")
        self.cpp_info.exelinkflags.append("-framework AudioToolbox")
        self.cpp_info.exelinkflags.append("-framework Foundation")
        self.cpp_info.exelinkflags.append("-framework AppKit")
        self.cpp_info.exelinkflags.append("-framework AVFoundation")
        self.cpp_info.exelinkflags.append("-framework CoreGraphics")
        self.cpp_info.exelinkflags.append("-framework QuartzCore")
        self.cpp_info.exelinkflags.append("-framework CoreVideo")
        self.cpp_info.exelinkflags.append("-framework CoreMedia")
        self.cpp_info.exelinkflags.append("-framework VideoToolbox")

        self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
