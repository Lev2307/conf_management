local year = 20;
local defGroupNum = 4;
local group(n) = "ИКБО-%d-%d" % [n, year];

{
    groups: ["ИКБО-%d-%d" % [i, year] for i in std.range(1, 24)],
    students: [
        {
            "age": 19,
            "group": group(defGroupNum),
            "name" : "Иванов И.И.",
        },
        {
            "age": 18,
            "group": group(defGroupNum+1),
            "name" : "Петров П.П.",
        },
        {
            "age": 18,
            "group": group(defGroupNum+1),
            "name" : "Сидоров С.С.",
        },
        {
            "age": 20,
            "group": group(defGroupNum-1),
            "name" : "Родионов Р.Р.",
        }
    ],
    subject: "Конфигурационное управление",
}