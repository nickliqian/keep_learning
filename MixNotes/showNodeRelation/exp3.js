var dataset = {
        nodes: [
                { name: "Adam" },
                { name: "Bob" },
                { name: "Carrie" },
                { name: "Donovan" },
                { name: "Edward" },
                { name: "Felicity" },
                { name: "George" },
                { name: "Hannah" },
                { name: "Iris" },
                { name: "Jerry" }
        ],
        links: [
                { source: 0, target: 1 },
                { source: 0, target: 2 },
                { source: 0, target: 3 },
                { source: 0, target: 4 },
                { source: 1, target: 5 },
                { source: 2, target: 5 },
                { source: 2, target: 5 },
                { source: 3, target: 4 },
                { source: 5, target: 8 },
                { source: 5, target: 9 },
                { source: 6, target: 7 },
                { source: 7, target: 8 },
                { source: 8, target: 9 }
        ]
};

var svg = d3.select('svg'),
		width = +svg.attr('width'),
		height = +svg.attr('height'),
		colors = d3.scaleOrdinal(d3.schemeCategory10);

var simulation = d3.forceSimulation(dataset.nodes)
                   .force("charge", d3.forceManyBody().strength(-600).distanceMax(330).theta(0))
                   .force('link', d3.forceLink(dataset.links).distance(130))
                   .force('center', d3.forceCenter(width / 2, height / 2))
														.force("collide", d3.forceCollide().radius(35));

var link = svg.append('g')
               .attr('class', 'links')
              .selectAll('line')
              .data(dataset.links)
              .enter().append('line')
               .attr('stroke', '#ccc')
               .attr('stroke-width', 1);

var node = svg.append('g')
                .attr('class', 'nodes')
              .selectAll('circle')
              .data(dataset.nodes)
              .enter().append('circle')
                .attr('r', 10)
                .attr('fill', function(d, i) {
									return colors(i);
								})
                .call(d3.drag()
										 .on('start', dragstarted)
										 .on('drag', dragged)
										 .on('end', dragended));

node.append('title')
    .text(function(d) { return d.name; });

simulation
    .nodes(dataset.nodes)
    .on('tick', ticked);

simulation.force('link')
          .links(dataset.links);

function ticked() {
	link
			.attr('x1', function(d) { return d.source.x; })
			.attr('y1', function(d) { return d.source.y; })
			.attr('x2', function(d) { return d.target.x; })
			.attr('y2', function(d) { return d.target.y; })

	node
			.attr('cx', function(d) { return d.x; })
			.attr('cy', function(d) { return d.y; })
}

function dragstarted(d) {
	if (!d3.event.active) simulation.alphaTarget(0.3).restart();
	d.fx = d.x;
	d.fy = d.y;
}

function dragged(d) {
	d.fx = d3.event.x;
	d.fy = d3.event.y;
}

function dragended(d) {
	if (!d3.event.active) simulation.alphaTarget(0);
	d.fx = null;
	d.fy = null;
}