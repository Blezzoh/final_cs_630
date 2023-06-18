
const {data} = require("./Posts")
const fs = require('fs')
const transform = ( i) =>{
    let b = data[Math.floor(Math.random() * 10000)].Body
    return {
        "id":i,
        "CreationDate": "2012-02-08T20:02:48.790",
        "PostId": Math.floor(Math.random() * 100),
        "RelatedPostId":Math.floor(Math.random() * 100),
        "LinkTypeId": 6
     } 
}

let d = []

for (let i =1; i < 1292 ; i++){
    d.push(transform(i))
}

fs.writeFile('output.json', JSON.stringify(d), (err) => {
          
    // In case of a error throw err.
    if (err) throw err;
})