const unique = (value, index, self) => {
    return self.indexOf(value) === index
}

function createMap(data) {
  console.log(data);
  //code here for Map
  //var types = ["","","","","","","",""];
  var types = data.map(x => x.type);
  var uniqueTypes = types.filter(unique);
  var types_pre = [];
  for (i=0; i < uniqueTypes.length; i++) {
    types_pre = types_pre.concat("");
  }
  types = types_pre.concat(types);
  var breeds = uniqueTypes.concat(data.map(x => x.breeds.primary));
 /*  var sizes = data.map(x => {
      if (x.size=="Small") {
          return 1
      }
      else if (x.size=="Medium") {
          return 2
      }
      else if (x.size=="Large") {
          return 3
      }
      else if (x.size=="Extra Large") {
          return 4
      }
      else {
          return 0
      }
  }); */
  console.log(types);
  console.log(breeds);
  
  var data1 = [{
      type: "sunburst",
      //maxdepth: -1,
      labels: breeds,
      parents: types,
      count: "branches+leaves",
      //level: "",
      //values: sizes,
      //branchvalues: "total",
      //outsidetextfont: {size: 20, color: "#377eb8"},
      //leaf: {opacity: 0.4},
      marker: {line: {width: 0}},
      //textposition: 'inside',
      //insidetextorientation: 'radial'
  }];

  var layout = {
      margin: {l: 0, r: 0, b: 0, t: 0},
      /* sunburstcolorway:[
        "#636efa","#EF553B","#00cc96","#ab63fa","#19d3f3",
        "#e763fa", "#FECB52","#FFA15A","#FF6692","#B6E880"
      ],
      extendsunburstcolorway: true */
      /* width: 500,
      height: 500 */
  };

  Plotly.newPlot('map', data1, layout, {showSendToCloud: true});
}