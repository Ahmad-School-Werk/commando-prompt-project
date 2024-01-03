import os
import sys
import time
import cmd
import requests
import shutil
import pytube

users = []
download_version = "0.1.3"
version_install = "0.1.2"
app_version = "1.0.0"


class CodeLanguages:
    """Class to define programming languages with information and ANSI codes for terminal output."""

    LANGUAGES_INFO = {
        'Python': 'Python is a high-level, interpreted programming language known for its readability and versatility.',
        'C++': 'C++ is a general-purpose programming language that supports object-oriented programming.',
        'TypeScript': 'TypeScript is a superset of JavaScript that adds static typing to the language.',
        'Ruby': 'Ruby is a dynamic, object-oriented programming language with a focus on simplicity and productivity.',
        'Ada': 'Ada is a high-level programming language used in safety-critical systems.',
        'Cobol': 'COBOL (Common Business Oriented Language) is a language used for business, finance, and administrative systems.',
        'PowerShell': 'PowerShell is a task automation framework from Microsoft with a command-line shell and scripting language.',
        'LISP': 'LISP (List Processing) is a family of programming languages known for their unique code-as-data and data-as-code philosophy.',
        'Erlang': 'Erlang is a functional programming language designed for concurrent and distributed systems.',
        'Java': 'Java is a general-purpose, object-oriented programming language known for its portability and platform independence.',
        'PHP': 'PHP is a server-side scripting language designed for web development.',
        'MATLAB': 'MATLAB is a programming language and environment used for numerical computing and data analysis.',
        'Scala': 'Scala is a statically-typed programming language that combines object-oriented and functional programming paradigms.',
        'Lua': 'Lua is a lightweight, embeddable scripting language designed for extensibility and performance.',
        'Julia': 'Julia is a high-level, high-performance programming language for technical computing.',
        'SQL': 'SQL (Structured Query Language) is a domain-specific language used for managing and manipulating relational databases.',
        'Ballerina': 'Ballerina is a cloud-native programming language designed for building resilient and scalable services.',
        'Speakeasy': 'Speakeasy is a dynamically-typed scripting language for building macOS applications.',
        'JavaScript': 'JavaScript is a scripting language widely used for web development.',
        'R': 'R is a programming language and environment for statistical computing and graphics.',
        'Kotlin': 'Kotlin is a statically-typed programming language that runs on the Java Virtual Machine (JVM).',
        'Visual Basic': 'Visual Basic is an event-driven programming language and integrated development environment from Microsoft.',
        'Abap': 'ABAP (Advanced Business Application Programming) is a high-level programming language used in SAP software.',
        'Haskell': 'Haskell is a purely functional programming language with strong static typing and lazy evaluation.',
        'Clojure': 'Clojure is a dialect of Lisp that runs on the Java Virtual Machine (JVM).',
        'FORTRAN': 'FORTRAN (Formula Translation) is a programming language for numerical and scientific computing.',
        'Simula': 'Simula is a programming language designed for simulation and modeling.',
        'Eiffel': 'Eiffel is an object-oriented programming language known for its design-by-contract methodology.',
        'C#': 'C# (C-sharp) is a modern, object-oriented programming language developed by Microsoft.',
        'Objective-C': 'Objective-C is an object-oriented programming language used for macOS and iOS development.',
        'Go': 'Go (Golang) is a statically-typed, compiled programming language developed by Google.',
        'Rust': 'Rust is a systems programming language known for its focus on safety and performance.',
        'Groovy': 'Groovy is a dynamic programming language for the Java Virtual Machine (JVM).',
        'Delphi': 'Delphi is a programming language and integrated development environment for Windows applications.',
        'Elixir': 'Elixir is a functional, concurrent programming language built on the Erlang virtual machine.',
        'BASIC': 'BASIC (Beginner\'s All-purpose Symbolic Instruction Code) is a family of high-level programming languages.',
        'Smalltalk': 'Smalltalk is an object-oriented programming language known for its simplicity and flexibility.',
        'Rebol': 'Rebol is a lightweight, dynamically-typed programming language for domain-specific languages.',
        'Swift': 'Swift is a modern, open-source programming language developed by Apple for iOS, macOS, and more.',
        'VBA': 'VBA (Visual Basic for Applications) is a programming language developed by Microsoft for automation in Microsoft Office.',
        'Dart': 'Dart is a programming language developed by Google for building mobile, desktop, server, and web applications.',
        'Perl': 'Perl is a high-level, general-purpose programming language known for its text processing capabilities.',
        'Elm': 'Elm is a functional programming language for building web front-end applications.',
        'Pascal': 'Pascal is a procedural programming language designed for teaching programming concepts.',
        'Alice': 'Alice is an educational programming language designed to teach programming in a 3D environment.',
        'Prolog': 'Prolog is a logic programming language used for artificial intelligence and symbolic reasoning.',
        'Scratch': 'Scratch is a visual programming language designed for teaching programming concepts to beginners.',
        # ... Add more languages as needed
    }

    ANSI_CODES = {
        'Python': '\033[92m',  # Green
        'C++': '\033[94m',      # Blue
        'TypeScript': '\033[96m',  # Cyan
        'Ruby': '\033[91m',      # Red
        'Ada': '\033[93m',       # Yellow
        'Cobol': '\033[95m',     # Magenta
        'PowerShell': '\033[97m', # White
        'LISP': '\033[35m',      # Purple
        'Erlang': '\033[36m',    # Cyan
        'Java': '\033[33m',      # Yellow
        'PHP': '\033[34m',       # Blue
        'MATLAB': '\033[32m',    # Green
        'Scala': '\033[31m',     # Red
        'Lua': '\033[30m',       # Black
        'Julia': '\033[37m',     # White
        'SQL': '\033[95m',       # Magenta
        'Ballerina': '\033[33m', # Yellow
        'Speakeasy': '\033[90m', # Dark Gray
        'JavaScript': '\033[93m', # Yellow
        'R': '\033[91m',         # Red
        'Kotlin': '\033[92m',     # Green
        'Visual Basic': '\033[94m', # Blue
        'Abap': '\033[95m',         # Magenta
        'Haskell': '\033[35m',      # Purple
        'Clojure': '\033[96m',      # Cyan
        'FORTRAN': '\033[36m',      # Cyan
        'Simula': '\033[37m',       # White
        'Eiffel': '\033[31m',       # Red
        'C#': '\033[33m',           # Yellow
        'Objective-C': '\033[34m',   # Blue
        'Go': '\033[92m',            # Green
        'Rust': '\033[91m',          # Red
        'Groovy': '\033[95m',        # Magenta
        'Delphi': '\033[93m',        # Yellow
        'Elixir': '\033[36m',        # Cyan
        'BASIC': '\033[32m',         # Green
        'Smalltalk': '\033[31m',     # Red
        'Rebol': '\033[30m',         # Black
        'Swift': '\033[37m',         # White
        'VBA': '\033[90m',           # Dark Gray
        'Dart': '\033[33m',          # Yellow
        'Perl': '\033[34m',          # Blue
        'Elm': '\033[32m',           # Green
        'Pascal': '\033[31m',        # Red
        'Alice': '\033[91m',         # Red
        'Prolog': '\033[95m',        # Magenta
        'Scratch': '\033[96m',       # Cyan
        # ... Add ANSI codes for more languages
    }

    def get_info(self, language):
        """Get information about a specific programming language."""
        return self.LANGUAGES_INFO.get(language, f'Information about {language} not available.')

    def get_ansi_code(self, language):
        """Get ANSI code for a specific programming language."""
        return self.ANSI_CODES.get(language, f'ANSI code for {language} not available.')

class Code_laguisches:
    "Class to define ANSI languisches names abd codes for terminal output."
    PYTHON = """
    name = "python"
    print(name)    

    name[0] = 'Python'
    name[1] = 'c++'
    print(f"N0: {name[0]}, N1: {name[1]})

"""

class Hacker:
    pass

class Animations:
    def __init__(self):
        pass

    def loading_animation(self, duration=10, sleep = 0.1):
        animation_frames = ['|', '/', '-', '\\']
        for _ in range(duration):
            for frame in animation_frames:
                print(f'\rLoading... {frame}', end='', flush=True)
                time.sleep(sleep)
        print('\nDone!')

class Colors:
    """Class to define ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    END = '\033[0m'
    YELLOW = '\033[93m'

class App:
    def __init__(self, name, number):
        self.name = name
        self.number = number

class UserManagement:
    """Class to manage user-related operations."""
    def __init__(self):
        self.users = users
        self.password = "1029384756"

    def add_user(self):
        """Add a new user."""
        print(f"{Colors.GREEN}---Add User---{Colors.END}")
        entered_password = input(f'Enter Password (INT): {Colors.YELLOW}')

        if not entered_password.isdigit():
            print(f"{Colors.RED}Password must be an integer!{Colors.END}")
            return 0

        entered_password = int(entered_password)

        if entered_password == int(self.password):
            print(f"{Colors.GREEN}Correct!{Colors.END}")
            input(f"All Users:\n {self.users}\nPress Enter to continue...")
            new_user = input(f"{Colors.GREEN}Username to add: {Colors.YELLOW} ")
            self.users.append(new_user)
            print(f"{Colors.GREEN}Users:{Colors.END} {self.users}")
        else:
            print(f"{Colors.RED}Incorrect password!{Colors.END}")
            input("Press Enter to continue...")

    def clear(self):
        """Clear the console."""
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'nt':
            os.system('cls')

class Hacker:
    def __init__(self):
        pass

class Inputs:
    def __init__(self, functie, functies):
        self.functie = functie
        self.functies = functies
        if self.functie == '':
            self.functie = '26219ef2-e9de-49a7-a47d-b51d2d2197ee'
        elif self.functie == 'exit':
            self.functies["exit"]()
        elif self.functie == 'clear' or self.functie == 'cls':
            self.functies["clear"]()
        elif self.functie == 'add user':
            self.functies["add user"]()
        elif self.functie.split()[0] == 'install':
            self.functies["install"](self.functie)
        elif self.functie.split()[0] == 'download':
            self.functies["download"](self.functie)
        elif self.functie == 'info':
            self.functies["info"]()
        elif self.functie == 'programing languages':
            self.functies["programing languages"]()
        elif self.functie == 'version':
            self.functies["version"]()
        elif self.functie == 'help':
            self.functies["help"]()
        elif self.functie.split()[0] == "IF":
            self.functies["IF"](self.functie)
        elif self.functie.split()[0] == "cleaning":
            self.functies["cleaning"](self.functie)
        elif self.functie == '26219ef2-e9de-49a7-a47d-b51d2d2197ee':
            pass
        elif self.functie == "apps":
            self.functies["apps"]()
        elif self.functie == "Hacker":
            self.functies["Hacker"]()
        elif self.functie == "pip":
            self.functies["pip"](self.functie)
        elif self.functie in self.functies:
            self.functies[self.functie]()
        else:
            print(f"{Colors.RED}The term '{self.functie}' is not recognized.{Colors.END}")


class Models(UserManagement):
    """Class that extends UserManagement and defines specific functionality."""
    def __init__(self, functie):
        super().__init__()
        self.functie = functie
        self.functies = {
            "exit": self.exit,
            "clear": self.clear,
            "add user": self.add_user,
            "install": self.install,
            "download": self.download_youtube,
            "info": self.get_language_info,
            "programing languages": self.programing_languages,
            "version": self.version,
            "help": self.help,
            "IF": self.if_else,
            "cleaning" : self.cleaning,
            "apps" : self.download_our_app_message,
            "Hacker": Hacker,
            "pip":self.pip,
        }
        self.Animations = Animations()

    def process_input(self):
        """Process user input."""
        Inputs(self.functie, self.functies)

    def exit(self):
        """Exit the program."""
        sys.exit()

    def extract_link(self):
        """Extract the link from the command."""
        if len(self.functie.split()) == 2:
            return self.functie.split()[1]
        elif len(self.functie.split()) == 2 and self.functie.split()[1] == "--version":
            return "version"
        else:
            return None

    def install(self, functie):
        """Install a package."""
        download_link = self.extract_link()
        if download_link is not None and download_link != "--version":
            print(f"{Colors.YELLOW}Downloading from {download_link}...{Colors.END}")

            try:
                response = requests.get(download_link)
                response.raise_for_status()

                file_name = os.path.join(os.getcwd(), download_link.split('/')[-1])
                file_name = f"{file_name}.html"

                with open(file_name, 'wb') as f:
                    f.write(response.content)
                    
                    

                print(f"{Colors.GREEN}Download successful! File saved as {file_name}.{Colors.END}")
                self.code_spaces(file_name)

            except requests.RequestException as e:
                print(f"{Colors.RED}Failed to download from {download_link}: {str(e)}{Colors.END}")
        elif download_link == "--version":
            print(f"install version {version_install} from {sys.path[6]}")
        else:
            print(f"{Colors.RED}Incorrect link!{Colors.END}")

    def code_spaces(self, file):
        with open(file, 'r') as f:
            file_content =  f.read()
            file_content = file_content.split()
        
        print(file_content)

    def download_youtube(self, functie):
        """Download a video from YouTube."""
        download_link = self.extract_link()

        if download_link is not None and download_link != "--version":
            print(f"{Colors.YELLOW}Downloading from {download_link}...{Colors.END}")

            try:
                yt = pytube.YouTube(download_link)
                video = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
                video.download()
                self.on_download_complete(video)
                print(f"{Colors.GREEN}Download successful! Video saved as {video.title}.{Colors.END}")
            except Exception as e:
                print(f"{Colors.RED}Failed to download from {download_link}: {str(e)}{Colors.END}")
        elif download_link == "--version":
            print(f"download version {download_version} from {sys.path[6]}")
        else:
            print(f"{Colors.RED}Incorrect link!{Colors.END}")

    def on_download_complete(self, video):
        """Open the downloaded video."""
        os.system(f'open "{os.path.join(os.getcwd(), video.title)}.mp4"')  # For macOS
    
    def programing_languages(self):
        """Display a list of supported programming languages."""
        print(f"{Colors.GREEN}--- Supported Programming Languages ---{Colors.END}")
        for language in CodeLanguages.LANGUAGES_INFO:
            print(f"{Colors.GREEN}{language}{Colors.END}")

    
    def version(self):
        """Display the version information of the app."""
        print(f"{Colors.GREEN}App Version: {app_version}{Colors.END}")
    
    def help(self):
        """Display help information."""
        print(f"{Colors.GREEN}--- Help ---{Colors.END}")
        print("Available Commands:")
        print(" - add user: Add a new user.")
        print(" - clear (or cls): Clear the console.")
        print(" - exit: Exit the program.")
        print(" - install <link>: Install a package from the specified link.")
        print(" - download <link>: Download a YouTube video from the specified link.")
        print(" - IF download <link> ELSE <link> NONE: Download a YouTube video from the specified link. IF link one oke? download elif link two download else NONE")
        print(" - info <language>: Get information about a specific programming language.")
        print(" - programing_languages: Display a list of supported programming languages.")
        print(" - version: Display the version information of the app.")
        print(" - cleaning temp folders: Cleaning your combuter from pad files-folders.")
        print(" - help: Display this help message.")
    
    def get_language_info(self):
        """Get information about a specific programming language."""
        language = input(f"{Colors.YELLOW}Enter the programming language: {Colors.END}")
        print(CodeLanguages().get_info(language))
    
    def if_else(self, functie):
        """ 'IF download <link> ELSE <link> NONE'  Download a video from YouTube. """
        if functie.split()[0] == "IF" and len(functie.split()) == 5:
            if  functie.split()[3] == "ELSE":
                if functie.split()[2] and functie.split()[5]:
                    print("Oke")
                    download_link = functie.split()[2]
                    


                    if download_link is not None:
                        print(f"{Colors.YELLOW}Downloading from {download_link}...{Colors.END}")

                        try:
                            yt = pytube.YouTube(download_link)
                            video = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
                            video.download()
                            self.on_download_complete(video)
                            print(f"{Colors.GREEN}Download successful! Video saved as {video.title}.{Colors.END}")
                        except Exception as e:
                            print(f"{Colors.RED}Failed to download from {download_link} this is the firste: {str(e)}{Colors.END}")
                            download_link = functie.split()[5]
                            try:
                                yt = pytube.YouTube(download_link)
                                video = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
                                video.download()
                                self.on_download_complete(video)
                                print(f"{Colors.GREEN}Download successful! Video saved as {video.title}.{Colors.END}")
                            except Exception as e:
                                print(f"{Colors.RED}Failed to download from {download_link} this is the last: {str(e)}{Colors.END}")
                        

                    elif download_link == "--version":
                        print(f"download version {download_version} from {sys.path[6]}")
                    else:
                        print(f"{Colors.RED}Incorrect link!{Colors.END}")
                            
        pass

    def cleaning(self, functie):
        if len(functie.split()) > 1:
            print(f"{Colors.RED}Did you mean 'cleaning'? {Colors.END}")
        else:
             print("  -cleaning temp folders(1)")
             print(f"{Colors.RED}type only the number!{Colors.END}")
             func = int(input("Type clean: "))
             if func == 1:
                 self.schoon_temp_map()

    def schoon_temp_map(self):
        self.Animations.loading_animation()
        try:
            # Pad naar de systeemtemp-map verkrijgen
            temp_map_pad = os.path.join(os.environ['SystemRoot'], 'Temp')

            # Explorer openen in de temp-map
            os.system(f'explorer.exe {temp_map_pad}')

            # Alle bestanden en mappen in de temp-map verwijderen
            for root, dirs, files in os.walk(temp_map_pad):
                for bestand in files:
                    bestand_pad = os.path.join(root, bestand)
                    os.remove(bestand_pad)
                for map in dirs:
                    map_pad = os.path.join(root, map)
                    shutil.rmtree(map_pad)

            print(f"Temp-map opgeruimd: {temp_map_pad}")
        except Exception as e:
            print(f"Fout bij het opruimen van de temp-map: {e}")
    
    def download_our_app_message(self):
        print(f"{Colors.GREEN}--- Our Apps Desktop ---{Colors.END}")
        app = App("Talk to Function App", 1)
        print(f"{app.name} \n    -to download this app type (app {app.number} download)")
        app = App("Scanner App", 2)
        print(f"{app.name} \n    -to download this app type (app {app.number} download)")
        app = App("HTML, CSS, and JS Editor", 3)
        print(f"{app.name} \n    -to download this app type (app {app.number} download)")
    
    def pip(self, functie):
        if functie.split()[0] == "pip" and len(functie.split()) > 1:
            if functie.split()[1] == "install":
                pass
            else:
                print(f"{Colors.RED}This term is  failed!{Colors.END}")
        
    
    def use_our_code(self, functie):
        """Letting downloading our library."""
        lib_file_path = 'lib.py'
        devtermenal_file_path = 'devtermenal.py'

        try:
            with open(lib_file_path, 'r') as lib_file:
                lib_code = lib_file.read()

            with open(devtermenal_file_path, 'w+') as devtermenal_file:
                devtermenal_file.write(lib_code)

            print(f"{Colors.GREEN}Code copied successfully from lib.py to devtermenal.py.{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}Error copying code: {str(e)}{Colors.END}")
    