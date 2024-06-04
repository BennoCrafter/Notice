function jsonToHtml(jsonData) {
    let html = "";
    for (const node of jsonData.children) {
      switch (node.type) {
        case "node-header":
          html += `<h1>${node.children[0].content}</h1>`;
          break;
        case "node-new_line":
          html += "<br>";
          break;
        case "node-bold":
          html += `<b>${node.children[0].content}</b>`;
          break;
        case "TextNode":
          html += node.content;
          break;
        case "node-link":
          html += `<a href="${node.children[0].content}">${node.children[0].content}</a>`;
          break;
        case "node-list":
        html += "<ul>"; // Start unordered list
        if (node.content) { // Check for content property
            html += node.content; // Add content if present
        }
        for (const item of node.children) {
            console.log(item)
            if (item.type !== "TextNode"){
                html += `<li>${jsonToHtml(item)}</li>`;
            }else{
                html += `<li>${item.content}</li>`;
            }
        }
        html += "</ul>"; // End unordered list
        break;

        default:
          console.warn(`Unknown node type: ${node.type}`);
      }
    }
    return html;
  }
  const fs = require('fs');

  async function readFile(filePath) {
    return new Promise((resolve, reject) => {
      fs.readFile(filePath, 'utf-8', (err, data) => {
        if (err) {
          reject(err);
        } else {
          resolve(data);
        }
      });
    });
  }

(async () => {
try {
    const jsonData = await readFile("pythonTrans/example.json");
    const htmlContent = jsonToHtml(JSON.parse(jsonData));
    console.log(htmlContent);

} catch (err) {
    console.error(err);
}
})();