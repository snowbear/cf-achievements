class DID_NOT_SCRATCH_ME:
    id = 1
    name = "You didn't even scratch me!"
    description = "Have one of your submissions unsuccessfully challenged by [user:tourist]. There should be no successful hack attempts from [user:tourist] of your submissions for this problem."
    
class PERESVET:
    id = 2
    name = "Peresvet & Temir-murza"
    description = "Together with some other contestant mutually hack each other's submissions on the same problem. Hacked submissions should be the last submissions on this problem for both of you."
    
class POLYGLOT:
    id = 3
    name = "Polyglot"
    description = "In a rated for you contest get problems accepted in at least two different programming languages. Different variations or versions of the same language are not considered as different languages."

class LANGUAGE_DOES_NOT_MATTER:
    id = 4
    name = "Language does not matter"
    description = "Solve at least two problems in Unknown Language Round"

class SPECK_IN_YOUR_BROTHERS_EYE:
    id = 5
    name = "Speck in your brother's eye"
    description = "Hack somebody's solution and get your own solution failed during system tests on the same problem."

problems_for_language_achievement = 50

def get_language_achievement_description(language):
    return "Solve at least %d problems as official contestant in %s" % (problems_for_language_achievement , language)

def get_award_comment(language):
    return "solving %d problems in %s" % (problems_for_language_achievement , language)
    
class LANGUAGE_ACHIEVEMENT_C:
    id = 100
    name = "See the solution"
    lang = "C"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)
    
class LANGUAGE_ACHIEVEMENT_CPP:
    id = 101
    name = "Mainstream guy"
    lang = "C++"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)
    
class LANGUAGE_ACHIEVEMENT_CS:
    id = 102
    name = "It's not a chord!"
    lang = "C#"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)
    
class LANGUAGE_ACHIEVEMENT_D:
    id = 103
    name = "Just D it!"
    lang = "D"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)
    
class LANGUAGE_ACHIEVEMENT_GO:
    id = 104
    name = "GOogled the answer"
    lang = "Go"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)
    
class LANGUAGE_ACHIEVEMENT_HASKELL:
    id = 105
    name = "Lambda's best friend"
    lang = "Haskell"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)

class LANGUAGE_ACHIEVEMENT_JAVA:
    id = 106
    name = "Runs on billions of devices... Slowly"
    lang = "Java"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)
    
class LANGUAGE_ACHIEVEMENT_OCAML:
    id = 107
    name = "Trip across the desert"
    lang = "OCaml"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)
        
class LANGUAGE_ACHIEVEMENT_PASCAL:
    id = 109
    name = "Tourist's path"
    lang = "Pascal or Delphi"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)
    
class LANGUAGE_ACHIEVEMENT_PERL:
    id = 110
    name = "Casting perls"
    lang = "Perl"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)
    
class LANGUAGE_ACHIEVEMENT_PHP:
    id = 111
    name = "Picked the Hard Path"
    lang = "PHP"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)
    
class LANGUAGE_ACHIEVEMENT_PYTHON:
    id = 112
    name = "Parselmouth"
    lang = "Python"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)
    
class LANGUAGE_ACHIEVEMENT_RUBY:
    id = 113
    name = "Gem among stones"
    lang = "Ruby"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)

class LANGUAGE_ACHIEVEMENT_SCALA:
    id = 114
    name = "Made in Switzerland"
    lang = "Scala"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)

class LANGUAGE_ACHIEVEMENT_JAVASCRIPT:
    id = 115
    name = "Web programmer"
    lang = "JavaScript"
    description = get_language_achievement_description(lang)
    award_comment = get_award_comment(lang)

language_achievements = [ 
                            LANGUAGE_ACHIEVEMENT_C , 
                            LANGUAGE_ACHIEVEMENT_CPP ,
                            LANGUAGE_ACHIEVEMENT_CS ,
                            LANGUAGE_ACHIEVEMENT_D ,
                            LANGUAGE_ACHIEVEMENT_GO ,
                            LANGUAGE_ACHIEVEMENT_HASKELL ,
                            LANGUAGE_ACHIEVEMENT_JAVA ,
                            LANGUAGE_ACHIEVEMENT_OCAML ,
                            LANGUAGE_ACHIEVEMENT_PASCAL ,
                            LANGUAGE_ACHIEVEMENT_PERL ,
                            LANGUAGE_ACHIEVEMENT_PHP ,
                            LANGUAGE_ACHIEVEMENT_PYTHON ,
                            LANGUAGE_ACHIEVEMENT_RUBY ,
                            LANGUAGE_ACHIEVEMENT_SCALA ,
                            LANGUAGE_ACHIEVEMENT_JAVASCRIPT ,
                            ]
    
def get_language_achievement_class(achievement):
    for ach in language_achievements:
        if ach.id == achievement.id:
            return ach
    raise Exception("bad achievement: %d" % achievement.id)