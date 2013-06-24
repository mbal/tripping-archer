import Debug.Trace

commands = ["q[uit]", "quita[ll]", "qa[ll]", "e[dit]", "w[rite]", "sav[eas]", "b[uffer]"]

lookup1 cmd = cmd

advance until (char:what) =
    if char == until
        then what
        else (advance until what)

advanceTill 0 s = s
advanceTill index (s:string) = advanceTill (index - 1) string

is string pattern = (helper string pattern False)

helper cmd ('[':pattern) optional = 
    if cmd == []
        then (advance ']' pattern) == []
        else (helper cmd pattern True)

helper cmd@(s:string) (']':pattern) optional = helper cmd pattern False

helper [] [] _ = True
helper _ [] _ = False

helper cmd@(s:string) (p:pattern) optional = 
    if optional
        then 
            let index = (optionalMatch cmd (p:pattern) 0) in
            if (index > 0) 
                then (helper (advanceTill index cmd) (advance ']' pattern) False)
                else (helper cmd (advance ']' pattern) False)
        else
            (s == p) && (helper string pattern optional)

optionalMatch _ [] i = i
optionalMatch [] _ i = i
optionalMatch _ (']':_) i = i
optionalMatch (s:string) (p:pattern) i =
    if (s == p)
        then (optionalMatch string pattern (i + 1))
        else 0

match _ [] = "undef"
match command (cmd:cmds) =
    if is command cmd 
        then lookup1 cmd
        else match command cmds
