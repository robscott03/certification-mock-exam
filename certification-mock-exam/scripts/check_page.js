// Usage: node check_page.js <exam.html>
const fs = require("fs");

const pagePath = process.argv[2];
const page = fs.readFileSync(pagePath, "utf8");
const pageScript = page.split("<script>")[1].split("</script>")[0];

new Function(pageScript);
console.log(`ok: ${pagePath} script parses`);
