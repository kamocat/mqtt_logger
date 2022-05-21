let settings = {
  curve = d3.curveLinear, // method of interpolation between points
  marginTop = 20, // top margin, in pixels
  marginRight = 30, // right margin, in pixels
  marginBottom = 30, // bottom margin, in pixels
  marginLeft = 40, // left margin, in pixels
  width = 640, // outer width, in pixels
  height = 400, // outer height, in pixels
  yFormat, // a format specifier string for the y-axis
  yLabel, // a label for the y-axis
  color = "currentColor", // fill color of area
  id= "#chart",
};
function InitChart( settings ){
	let div = d3.select(id);
    const svg = d3.create("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr("style", "max-width: 100%; height: auto; height: intrinsic;");
    svg.append("g")
            .attr("class", "yaxis")
            .attr("transform", `translate(${marginLeft},0)`)
            .call(yAxis)
            .call(g => g.select(".domain").remove())
            .call(g => g.selectAll(".tick line").clone()
                    .attr("x2", width - marginLeft - marginRight)
                    .attr("stroke-opacity", 0.1))
            .call(g => g.append("text")
                    .attr("x", -marginLeft)
                    .attr("y", 10)
                    .attr("fill", "currentColor")
                    .attr("text-anchor", "start")
                    .text(yLabel));
    svg.append("g")
            .attr("class", "xaxis")
            .attr("transform", `translate(0,${height - marginBottom})`)
            .call(xAxis);
    div.node().append(svg.node());
}
function updateAxes(alldata, conf){
  xRange = [conf.marginLeft, conf.width - conf.marginRight], // [left, right]
  yRange = [conf.height - conf.marginBottom, conf.marginTop], // [bottom, top]
  // Get min and max of x and y for all plots
  const X = data.time.map(x=>x*1000);
  const Y = data.value;

  // Compute default domains.
  xDomain = d3.extent(X);
  yDomain = [d3.min(Y), d3.max(Y)];

  // Construct scales and axes.
  conf.xScale = d3.scaleTime(xDomain, xRange);
  conf.yScale = d3.scaleLinear(yDomain, yRange);
  const xAxis = d3.axisBottom(conf.xScale).ticks(width / 80).tickSizeOuter(0);
  const yAxis = d3.axisLeft(conf.yScale).ticks(height / 40, yFormat);

    svg = d3.select("svg")
    svg = svg.transition().duration(750);
    svg.select(".yaxis").call(yAxis);
    svg.select(".xaxis").call(xAxis);
}
function make_line(data, settings){
    const I = d3.range(X.length);
    let line = d3.line()
      .curve(settings.curve)
      .x(i => settings.xScale(data.time[i]))
      .y(i => settings.yScale(data.value[i]));
    return line(data.time.length);
}
function addPlot(data, settings){
	svg.append("path")
                .attr("id", data.i)
				.attr("fill", "none")
				.attr("d", make_line(data,settings))
				.attr("stroke", settings.color)
				.attr("stroke-width", 1.5);
}
function updatePlot(data, settings){
    svg.select(".line").attr("d", make_line(data,settings));
}
function deletePlot(data, settings){
        d3.select("#"+ data.i).remove();
}
