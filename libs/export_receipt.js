const receiptline = require('receiptline');
const fs = require('fs');
const display = {
    cpl: 42,
    encoding: 'multilingual'
};
const printer = {
    cpl: 42,
    encoding: 'multilingual',
    upsideDown: false,
    gamma: 1.8,
    command: 'escpos'
};

// display example
fs.readFile('/tmp/tmpr5gzs39d', function(err, data) {
    doc = data.toString();
    const svg = receiptline.transform(doc, display);
    fs.writeFile('output.svg', svg, function (err) {
        if (err) throw err;
        console.log('Saved!');
      });
    
    // const command = receiptline.transform(doc, printer);
    // console.log(command);
    // fs.writeFile('output.cmd', command, function (err) {
    //     if (err) throw err;
    //     console.log('Saved!');
    //   });

  });


