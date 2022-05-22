let settings = {
  curve: d3.curveLinear, // method of interpolation between points
  marginTop: 20, // top margin, in pixels
  marginRight: 30, // right margin, in pixels
  marginBottom: 30, // bottom margin, in pixels
  marginLeft: 40, // left margin, in pixels
  width: 800, // outer width, in pixels
  height: 600, // outer height, in pixels
  color: "currentColor", // fill color of area
  id: "#chart",
};
function InitChart( conf ){
	let div = d3.select(settings.id);
    const svg = d3.create("svg")
            .attr("width", conf.width)
            .attr("height", conf.height)
            .attr("viewBox", [0, 0, conf.width, conf.height])
            .attr("style", "max-width: 100%; height: auto; height: intrinsic;");
    
    const xRange = [conf.marginLeft, conf.width - conf.marginRight]; // [left, right]
    const yRange = [conf.height - conf.marginBottom, conf.marginTop]; // [bottom, top]
    const domain = [-1,1];
    const xScale = d3.scaleLinear(domain, xRange);
    const yScale = d3.scaleLinear(domain, yRange);
    const xAxis = d3.axisBottom(xScale).ticks(conf.width / 80).tickSizeOuter(0);
    const yAxis = d3.axisLeft(yScale).ticks(conf.height / 40);
    svg.append("g")
            .attr("class", "yaxis")
            .attr("transform", `translate(${conf.marginLeft},0)`)
            .call(yAxis)
    svg.append("g")
            .attr("class", "xaxis")
            .attr("transform", `translate(0,${conf.height - conf.marginBottom})`)
            .call(xAxis);
    div.node().append(svg.node());
}
function updateAxes(alldata, conf){
    xRange = [conf.marginLeft, conf.width - conf.marginRight], // [left, right]
    yRange = [conf.height - conf.marginBottom, conf.marginTop], // [bottom, top]
                                                                       // Get min and max of x and y for all plots
    x = [];
    y = [];
    for (d in alldata){
        x.push(d3.min(alldata[d].time));
        x.push(d3.max(alldata[d].time));
        y.push(d3.min(alldata[d].value));
        y.push(d3.max(alldata[d].value));
    }

    // Compute default domains.
    xDomain = [d3.min(x)*1000, d3.max(x)*1000];
    yDomain = [d3.min(y), d3.max(y)];

    // Construct scales and axes.
    conf.xScale = d3.scaleTime(xDomain, xRange);
    conf.yScale = d3.scaleLinear(yDomain, yRange);
    const xAxis = d3.axisBottom(conf.xScale).ticks(conf.width / 80).tickSizeOuter(0);
    const yAxis = d3.axisLeft(conf.yScale).ticks(conf.height / 40);

    svg = d3.select("svg")
    svg = svg.transition().duration(750);
    svg.select(".yaxis").call(yAxis);
    svg.select(".xaxis").call(xAxis);

    // Fix the mapping on x axis
    xDomain = [d3.min(x), d3.max(x)];
    conf.xScale = d3.scaleTime(xDomain, xRange);
    
}
function make_line(data, settings){
    const I = d3.range(data.time.length);
    let line = d3.line()
      .curve(settings.curve)
      .x(i => settings.xScale(data.time[i]))
      .y(i => settings.yScale(data.value[i]));
    return line(I);
}
function addPlot(data, settings){
    d3.select("svg").append("path")
            .attr("id", data.i)
            .attr("fill", "none")
            .attr("d", make_line(data,settings))
            .attr("stroke", settings.color)
            .attr("stroke-width", 1.5);
}

function updatePlot(data, settings){
    plot = d3.select("#"+ data.i);
    if( plot.empty() ){
        addPlot(data, settings);
    } else {
        plot
            .transition().duration(750)
            .attr("d", make_line(data,settings));
    }
}

function updateAll(alldata, settings){
    updateAxes(data, settings);
    for (d in alldata){
        updatePlot(alldata[d], settings);
    }
}
function deletePlot(data, settings){
        d3.select("#"+ data.i).remove();
}
