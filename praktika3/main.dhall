let year = "20"
let defGroupNum = 4
let groupCount = 24

let group = \(n : Natural) -> "ИКБО-" ++ Natural/show n ++ "-" ++ year

let groups =
    Natural/fold 
      groupCount
      (List Text)
      ( \(acc : List Text) ->
            [ group (Natural/subtract (List/length Text acc) groupCount) ]
       #acc
      )
      ([]: List Text)
    
in  { subject = "Конфигурационное управление"
    , groups = groups
    , students = [ 
        { age = 19, group = "ИКБО-" ++ Natural/show (defGroupNum) ++ "-" ++ year, name = "Иванов И.И." },
        { age = 18, group = "ИКБО-" ++ Natural/show (defGroupNum + 1) ++ "-" ++ year, name = "Петров П.П." },
        { age = 18, group = "ИКБО-" ++ Natural/show (defGroupNum + 1) ++ "-" ++ year, name = "идоров С.С." },
        { age = 20, group = "ИКБО-" ++ Natural/show (Natural/subtract 1 defGroupNum) ++ "-" ++ year, name = "Родионов Р.Р." },
        ]
    }