
const width = 800,
      height = 800;

let state = {
  transient: [],
  selected: []
}

let svg = d3.select("body")
    .append("svg")
    .attrs({
      width: width,
      height: height
    }).on("mousemove", new_imgs);

svg.selectAll("g")
  .data(["points", "voronoi", "imgs"]).enter()
  .append("g");

let scales = {
  x: d3.scaleLinear().domain([-4, 4]).range([0, width]),
  y: d3.scaleLinear().domain([-4, 4]).range([0, height])
}
let voronoi = d3.voronoi().extent([[0, 0], [width, height]]);


d3.select("#points")
  .data(data).enter()
  .append("circle")
  .attrs({
    x: (d) => scales.x(d.x),
    y: (d) => scales.y(d.y),
    r: 2
  });

let polys = voronoi.polygons(data.map((d) => [d.x, d.y]));
d3.select("#")
