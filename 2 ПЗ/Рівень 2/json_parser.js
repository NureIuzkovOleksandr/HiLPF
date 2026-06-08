const readline = require('readline');

function parseJsonToTree(data, prefix = "", isLast = true) {
    let result = [];
    if (data !== null && typeof data === 'object') {
        if (Array.isArray(data)) {
            for (let i = 0; i < data.length; i++) {
                const item = data[i];
                const isLastItem = (i === data.length - 1);
                const connector = isLastItem ? "└── " : "├── ";
                const extension = isLastItem ? "    " : "│   ";
                if (item !== null && typeof item === 'object') {
                    result.push(`${prefix}${connector}[${i}] (${Array.isArray(item) ? 'Array' : 'Object'})`);
                    const treeStr = parseJsonToTree(item, prefix + extension, isLastItem);
                    result.push(treeStr);
                } else {
                    const typeName = item === null ? 'null' : typeof item;
                    const valRepr = item === null ? 'null' : (typeof item === 'string' ? `'${item}'` : String(item));
                    result.push(`${prefix}${connector}[${i}] ${valRepr} (${typeName})`);
                }
            }
        } else {
            const keys = Object.keys(data);
            for (let i = 0; i < keys.length; i++) {
                const key = keys[i];
                const value = data[key];
                const isLastItem = (i === keys.length - 1);
                const connector = isLastItem ? "└── " : "├── ";
                const extension = isLastItem ? "    " : "│   ";
                if (value !== null && typeof value === 'object') {
                    result.push(`${prefix}${connector}${key}: (${Array.isArray(value) ? 'Array' : 'Object'})`);
                    const treeStr = parseJsonToTree(value, prefix + extension, isLastItem);
                    result.push(treeStr);
                } else {
                    const typeName = value === null ? 'null' : typeof value;
                    const valRepr = value === null ? 'null' : (typeof value === 'string' ? `'${value}'` : String(value));
                    result.push(`${prefix}${connector}${key}: ${valRepr} (${typeName})`);
                }
            }
        }
    }
    return result.filter(line => line !== "").join("\n");
}

function analyzeJson(jsonStr) {
    try {
        const data = JSON.parse(jsonStr);
        console.log("=".repeat(70));
        console.log("JSON Аналіз");
        console.log("=".repeat(70));
        console.log("\nФорматований JSON:");
        console.log("-".repeat(70));
        console.log(JSON.stringify(data, null, 2));
        console.log("\n\nДеревоподібна структура:");
        console.log("-".repeat(70));
        console.log(parseJsonToTree(data));
        console.log("\n\nСтатистика:");
        console.log("-".repeat(70));
        const dataType = data === null ? 'null' : (Array.isArray(data) ? 'Array' : typeof data);
        console.log(`Тип: ${dataType}`);
        if (data && typeof data === 'object') {
            if (Array.isArray(data)) {
                console.log(`Кількість елементів: ${data.length}`);
            } else {
                console.log(`Кількість ключів: ${Object.keys(data).length}`);
            }
        }
    } catch (err) {
        console.log(`Помилка у JSON: ${err.message}`);
    }
}

function runDemo() {
    const testCases = [
        {
            name: "Простий об'єкт",
            json: '{"name": "John", "age": 30, "city": "Kyiv"}'
        },
        {
            name: "Вкладений об'єкт",
            json: '{"person": {"name": "John", "address": {"city": "Kyiv", "zip": "02000"}}, "active": true}'
        },
        {
            name: "Масив об'єктів",
            json: '[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]'
        },
        {
            name: "Складна структура",
            json: '{"users": [{"id": 1, "name": "Alice", "skills": ["Python", "JS"]}, {"id": 2, "name": "Bob", "skills": ["Java"]}], "total": 2}'
        }
    ];
    console.log("\n" + "=".repeat(70));
    console.log("ПРИКЛАДИ ПАРСИНГУ JSON");
    console.log("=".repeat(70) + "\n");
    testCases.forEach((test, idx) => {
        console.log(`\nПриклад ${idx + 1}: ${test.name}`);
        analyzeJson(test.json);
        console.log("\n" + "=".repeat(70));
    });
}

function startInteractiveMode() {
    console.log("\n\nІНТЕРАКТИВНИЙ РЕЖИМ");
    console.log("=".repeat(70));
    console.log("Введіть JSON-рядок для аналізу");
    console.log("Введіть 'exit' для виходу\n");
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
        prompt: 'JSON> '
    });
    rl.prompt();
    rl.on('line', (line) => {
        const userJson = line.trim();
        if (userJson.toLowerCase() === 'exit') {
            console.log("До побачення!");
            rl.close();
            return;
        }
        if (userJson) {
            analyzeJson(userJson);
            console.log();
        }
        rl.prompt();
    }).on('close', () => {
        process.exit(0);
    });
}

runDemo();
startInteractiveMode();
