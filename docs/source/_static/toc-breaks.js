// Furo lets long object names in the page contents wrap at any letter. A <wbr>
// after each dot and underscore makes them wrap between name parts first.
document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(".toc-tree a.reference");
  for (const link of links) {
    const walker = document.createTreeWalker(link, NodeFilter.SHOW_TEXT);
    const texts = [];
    while (walker.nextNode()) texts.push(walker.currentNode);
    for (const text of texts) {
      const parts = text.data.split(/(?<=[._])/);
      if (parts.length < 2) continue;
      const pieces = parts.flatMap((part, i) =>
        i ? [document.createElement("wbr"), part] : [part],
      );
      text.replaceWith(...pieces);
    }
  }
});
