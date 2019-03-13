from dragonfly import (Grammar, CompoundRule, Dictation, Text, Key, AppContext, MappingRule)


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
            Dictation('text')
    ]

    mapping = {
        "insert mode": Key("i"),
        "command mode": Key("escape"),
        "up": Key("up"),
        "down": Key("down"),
        "save file": Key("colon, w, enter"),
        "exit": Key("colon, q")
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
    if terminalGrammer: terminalGrammer.unload()
