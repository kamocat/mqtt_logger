// Copyright 2021 Observable, Inc.
// Released under the ISC license.
// https://observablehq.com/@d3/area-chart
function AreaChart(data, {
  defined, // given d in data, returns true if defined (for gaps)
  curve = d3.curveLinear, // method of interpolation between points
  marginTop = 20, // top margin, in pixels
  marginRight = 30, // right margin, in pixels
  marginBottom = 30, // bottom margin, in pixels
  marginLeft = 40, // left margin, in pixels
  width = 640, // outer width, in pixels
  height = 400, // outer height, in pixels
  xType = d3.scaleTime, // type of x-scale
  xDomain, // [xmin, xmax]
  xRange = [marginLeft, width - marginRight], // [left, right]
  yType = d3.scaleLinear, // type of y-scale
  yDomain, // [ymin, ymax]
  yRange = [height - marginBottom, marginTop], // [bottom, top]
  yFormat, // a format specifier string for the y-axis
  yLabel, // a label for the y-axis
  color = "currentColor", // fill color of area
  id= "div",
} = {}) {
  // Compute values.
  const X = data.time.map(x=>x*1000);
  const Y = data.value;
  const I = d3.range(X.length);

  // Compute default domains.
  if (xDomain === undefined) xDomain = d3.extent(X);
  if (yDomain === undefined) yDomain = [d3.min(Y), d3.max(Y)];

  // Construct scales and axes.
  const xScale = xType(xDomain, xRange);
  const yScale = yType(yDomain, yRange);
  const xAxis = d3.axisBottom(xScale).ticks(width / 80).tickSizeOuter(0);
  const yAxis = d3.axisLeft(yScale).ticks(height / 40, yFormat);

  // Construct an area generator.
  const area = d3.line()
      .curve(curve)
      .x(i => xScale(X[i]))
      .y(i => yScale(Y[i]));

	let div = d3.select(id);
	if(AreaChart.didrun){
		div = div.transition().duration(750);
		div.select(".line").attr("d", area(I));
		div.select(".yaxis").call(yAxis);
		div.select(".xaxis").call(xAxis);
	} else {
		AreaChart.didrun = true;
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

		svg.append("path")
				.attr("class", "line")
				.attr("fill", "none")
				.attr("d", area(I))
				.attr("stroke", color)
				.attr("stroke-width", 1.5);

		svg.append("g")
				.attr("class", "xaxis")
				.attr("transform", `translate(0,${height - marginBottom})`)
				.call(xAxis);

		div.node().append(svg.node());
	}
}
