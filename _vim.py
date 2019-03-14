from dragonfly import (Integer, IntegerRef, Grammar, CompoundRule, Dictation, Text, Key, AppContext, MappingRule)


class VimEnabler(CompoundRule):
    spec = "Enable visual grammar"  # Spoken command to enable the Vim grammar.

    def _process_recognition(self, node, extras):  # Callback when command is spoken.
        vimTerminalBootstrap.disable()
        terminalGrammer.enable()
        print "vim grammar enabled!"


class VimDisabler(CompoundRule):
    spec = "disable visual grammar"  # spoken command to disable the Vim grammar.

    def _process_recognition(self, node, extras):  # Callback when command is spoken.
        terminalGrammer.disable()
        vimTerminalBootstrap.enable()
        print "vim grammar disabled"

class VimCommands(MappingRule):

    extras = [
            Dictation('text'),
            IntegerRef("n", 1, 1000),
            IntegerRef("line", 1, 10000),
    ]

    defaults = {
        "n" : 1,
        "z" : 1,
     }

    mapping = {
        # Basic modes
        "insert mode": Key("i"),
        "command mode": Key("escape"),
        "save file": Key("colon, w, enter"),
        "quit": Key("colon, q"),

        # Navigation
        "up [<n>]" : Key("k:%(n)d"),
        "down [<n>]" : Key("j:%(n)d"),
        "left [<n>]" : Key("h:%(n)d"),
        "right [<n>]" : Key("l:%(n)d"),

        "go [<line>]": Key("colon") + Text("%(line)s\n"),
        
        # Basic commands
        "delete line" : Key("d,d"),
        "undo": Key("u"),
        "word [<n>]" : Key("w:%(n)d"),
        "back [<n>]" : Key("b:%(n)d"),
        "change word": Key("c,w"),

    }


# The main Vim grammar rules are activated here
vimTerminalBootstrap = Grammar("vim terminal bootstrap")
vimTerminalBootstrap.add_rule(VimEnabler())
vimTerminalBootstrap.load()

terminalGrammer = Grammar("vim grammar")
terminalGrammer.add_rule(VimCommands())
terminalGrammer.add_rule(VimDisabler())
terminalGrammer.load()
terminalGrammer.disable()

# Unload function which will be called by natlink at unload time.
def unload():
    global terminalGrammer
    if terminalGrammer: terminalGrammer.unload(),
