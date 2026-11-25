// Compile the deployed TeX with the same MathJax major version as the website.
const fs = require('fs');
const root = process.env.MATHJAX_ROOT || 'mathjax-full';
const {mathjax} = require(root + '/js/mathjax.js');
const {TeX} = require(root + '/js/input/tex.js');
const {SVG} = require(root + '/js/output/svg.js');
const {liteAdaptor} = require(root + '/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require(root + '/js/handlers/html.js');
for (const name of ['base/Base', 'ams/Ams', 'newcommand/Newcommand', 'configmacros/ConfigMacros']) {
  require(root + '/js/input/tex/' + name + 'Configuration.js');
}
const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const input = new TeX({packages: ['base', 'ams', 'newcommand', 'configmacros'], macros: {
  argmin: '\\operatorname*{arg\\,min}', argmax: '\\operatorname*{arg\\,max}',
  diag: '\\operatorname{diag}', rank: '\\operatorname{rank}', supp: '\\operatorname{supp}'
}});
const document = mathjax.document('', {InputJax: input, OutputJax: new SVG({fontCache: 'none'})});
const expressions = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const errors = [];
for (const expression of expressions) {
  const node = document.convert(expression.tex, {display: expression.display});
  const markup = adaptor.outerHTML(node);
  if (markup.includes('data-mjx-error') || markup.includes('merror')) {
    errors.push({...expression, error: markup.match(/data-mjx-error="([^"]*)"/)?.[1] || 'MathJax error'});
  }
}
console.log(JSON.stringify({expressions: expressions.length, errors}, null, 2));
if (errors.length) process.exitCode = 1;
