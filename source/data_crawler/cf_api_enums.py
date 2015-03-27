import json
import logging
import urllib.request
from enum import IntEnum

def enum_mapping(enum_type):
    return dict( [ ( e.name , e ) for e in enum_type ] )

class CONTEST_PHASE(IntEnum):
	BEFORE = 1
	CODING = 2
	PENDING_SYSTEM_TEST = 3
	SYSTEM_TEST = 4
	FINISHED = 5
contest_phase_mapping = enum_mapping(CONTEST_PHASE)

class PARTICIPANT_TYPE(IntEnum):
    CONTESTANT = 1
    PRACTICE = 2
    VIRTUAL = 3
    MANAGER = 4
    OUT_OF_COMPETITION = 5
participant_type_mapping = enum_mapping(PARTICIPANT_TYPE)

class HACK_VERDICT(IntEnum):
    HACK_SUCCESSFUL = 1
    HACK_UNSUCCESSFUL = 2
    INVALID_INPUT = 3
    GENERATOR_INCOMPILABLE = 4
    GENERATOR_CRASHED = 5
    IGNORED = 6
    TESTING = 7
    OTHER = 8
hack_verdict_mapping = enum_mapping(HACK_VERDICT)
        
class SUBMISSION_VERDICT(IntEnum):
    FAILED = 1
    OK = 2
    PARTIAL = 3
    COMPILATION_ERROR = 4
    RUNTIME_ERROR = 5
    WRONG_ANSWER = 6
    PRESENTATION_ERROR = 7
    TIME_LIMIT_EXCEEDED = 8
    MEMORY_LIMIT_EXCEEDED = 9
    IDLENESS_LIMIT_EXCEEDED = 10
    SECURITY_VIOLATED = 11
    CRASHED = 12
    INPUT_PREPARATION_CRASHED = 13
    CHALLENGED = 14
    SKIPPED = 15
    TESTING = 16
    REJECTED = 17
submission_verdict_mapping = enum_mapping(SUBMISSION_VERDICT)

class SUBMISSION_TESTSET(IntEnum):
    SAMPLES = 1
    PRETESTS = 2
    TESTS = 3
    CHALLENGES = 4
    TESTS1 = 105
    TESTS2 = 106
    TESTS3 = 107
    TESTS4 = 108
    TESTS5 = 109
    TESTS6 = 110
    TESTS7 = 111
    TESTS8 = 112
    TESTS9 = 113
    TESTS10 = 114
submission_testset_mapping = enum_mapping(SUBMISSION_TESTSET)

class LANGUAGE_GROUP(IntEnum):
	C = 1,
	Cpp = 2,
	CSharp = 3,
	D = 4,
	Go = 5,
	Haskell = 6,
	Java = 7,
	Ocaml = 8,
	Pascal = 10,
	Perl = 11,
	PHP = 12,
	Python = 13,
	Ruby = 14,
	Scala = 15,
	JavaScript = 16,
	FSharp = 17,
	Esoteric = 18,

class Language:
    def __init__(self, value, name, language_group):
        self.value = value
        self.name = name
        self.group = language_group

class Languages:        
    GnuC = Language(1, "GNU C", LANGUAGE_GROUP.C)
    GnuC11 = Language(27, "GNU C11", LANGUAGE_GROUP.C)
    GnuCpp = Language(2, "GNU C++", LANGUAGE_GROUP.Cpp)
    GnuCpp0x = Language(3, "GNU C++0x", LANGUAGE_GROUP.Cpp) # seems to be outdated
    GnuCpp11 = Language(4, "GNU C++11", LANGUAGE_GROUP.Cpp)
    MsCpp = Language(5, "MS C++", LANGUAGE_GROUP.Cpp)
    CSharpMs = Language(6, "MS C#", LANGUAGE_GROUP.CSharp)
    CSharpMono = Language(7, "Mono C#", LANGUAGE_GROUP.CSharp)
    D = Language(8, "D", LANGUAGE_GROUP.D)
    Go = Language(9, "Go", LANGUAGE_GROUP.Go)
    Haskell = Language(10, "Haskell", LANGUAGE_GROUP.Haskell)
    Java6 = Language(11, "Java 6", LANGUAGE_GROUP.Java)
    Java7 = Language(12, "Java 7", LANGUAGE_GROUP.Java)
    Java8 = Language(13, "Java 8", LANGUAGE_GROUP.Java)
    Ocaml = Language(14, "Ocaml", LANGUAGE_GROUP.Ocaml)
    Delphi = Language(15, "Delphi", LANGUAGE_GROUP.Pascal)
    FreePascal = Language(16, "FPC", LANGUAGE_GROUP.Pascal)
    Perl = Language(17, "Perl", LANGUAGE_GROUP.Perl)
    PHP = Language(18, "PHP", LANGUAGE_GROUP.PHP)
    Python2 = Language(19, "Python 2", LANGUAGE_GROUP.Python)
    Python3 = Language(20, "Python 3", LANGUAGE_GROUP.Python)
    Ruby = Language(21, "Ruby", LANGUAGE_GROUP.Ruby)
    Scala = Language(22, "Scala", LANGUAGE_GROUP.Scala)
    JavaScript = Language(23, "JavaScript", LANGUAGE_GROUP.JavaScript)
    FSharp = Language(24, "F#", LANGUAGE_GROUP.FSharp)
    PyPy2 = Language(25, "PyPy 2", LANGUAGE_GROUP.Python)
    PyPy3 = Language(26, "PyPy 3", LANGUAGE_GROUP.Python)
	
    Tcl = Language(100, "Tcl", LANGUAGE_GROUP.Esoteric)
    Io = Language(101, "Io", LANGUAGE_GROUP.Esoteric)
    Pike = Language(102, "Pike", LANGUAGE_GROUP.Esoteric)
    Befunge = Language(103, "Befunge", LANGUAGE_GROUP.Esoteric)
    Cobol = Language(104, "Cobol", LANGUAGE_GROUP.Esoteric)
    Ada = Language(105, "Ada", LANGUAGE_GROUP.Esoteric)
    Factor = Language(106, "Factor", LANGUAGE_GROUP.Esoteric)
    Roco = Language(107, "Roco", LANGUAGE_GROUP.Esoteric)
    FALSE = Language(108, "FALSE", LANGUAGE_GROUP.Esoteric)

    SecretLanguage = Language(150, "Mysterious Language", LANGUAGE_GROUP.Esoteric)

all_languages = [ val for val in Languages.__dict__.values() if type(val) == Language ]
language_mapping_dict_by_name = dict((l.name, l) for l in all_languages)
language_mapping_dict_by_value = dict((l.value, l) for l in all_languages)

def language_mapping(lang):
    if type(lang) == str:
        if lang.startswith("Secret"): return Languages.SecretLanguage
        return language_mapping_dict_by_name[lang]
    if type(lang) == int:
        return language_mapping_dict_by_value[lang]
    assert(False)