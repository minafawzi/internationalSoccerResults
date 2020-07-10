/*
*    main.js
*    FInal Project - FIFA historical analysis
*/

// first graph for the members pages

var margin = {left: 180, right: 20, top: 50, bottom: 100};
var height = 600 - margin.top -margin.bottom,
   width = 800 - margin.left - margin.right;

// Initialize the svg object
var svg1 = d3.select("#chart-area")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");    

// Appending the two labels (two boxes and two text)
    svg1.append("rect")
        .attr("height",20)
        .attr("width",200)
        .attr("x",2)
        .attr("y",480)
        .attr("fill","#096083");
        
    svg1.append("rect")
        .attr("height",20)
        .attr("width",200)
        .attr("x",242)
        .attr("y",480)
        .attr("fill","#3CA2CD");

    svg1.append("text")
        .attr("x",50 )
        .attr("y", 495)
        .text("FIFA Members")
        .attr("font-family", "sans-serif")
        .attr("font-size", "17px")
        .attr("fill", "white");

    svg1.append("text")
        .attr("x",290 )
        .attr("y", 495)
        .text("UN Members")
        .attr("font-family", "sans-serif")
        .attr("font-size", "17px")
        .attr("fill", "white");        

    // define Y coordinates (scale then axis)
    var y = d3.scaleLinear()
    .domain([10,230])
    .range([460,18]);

    var yLabel = svg1.append("text")
    .attr("y", -40)
    .attr("x", -190)
    .attr("font-size","20px")
    .attr("text-anchor", "middle")
    .attr("transform","rotate(-90)")
    .text("Members");

    var yAxis = d3.axisLeft(y)
    .tickFormat(function(coordsY1){return +coordsY1});
    svg1.append("g")
    .call(yAxis);


    // X coordinates of 10 circles of FIFA members and 10 circles of UN members (one from each after each other)
    // will use loop to repeat X coordinates by restting the array index for each row

    var coordsX2 = [10, 250, 30, 270, 50, 290, 70, 310, 90, 330, 110, 350, 130, 370, 150, 390, 170, 410, 190, 430]
     // Y coordinates of the circles 
    var coordsY1 = [10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330, 350, 370, 390, 410, 430, 450]


  var j=0;
  var i =0;
 
  var t = d3.interval(function(elapsed) {
    svg1.append("circle")
       .attr("cx", coordsX2[i] )
       .attr("cy", 490 - coordsY1[Math.floor(j/20)] - 10) // Index of Y coordinates array is calcualted to keep each 20 circles in the same horizontal line 
       .attr("r", 8)
       .attr("fill", (Math.floor(i%2 == 0)? (j<422)?"#096083":"#CAD4D8": (j<390)? "#3CA2CD":"#CAD4D8" ))  // two nested conditions UN vs FIFA and blank vs not
       .transition()
       .duration(0)
       .attr("cy", 490 - coordsY1[Math.floor(j/20)] - 20)
    i = i+1
    j = j+1
    if(i==20) i=0;
    if (j == 460) t.stop();
  }, 2);


  $({ Counter: 0 }).animate({
    Counter: $('.counter1').text()
  }, {
    duration: 2000,
    easing: 'swing',
    step: function() {
      $('.counter1').text(Math.ceil(this.Counter));
    }
  });

  $({ Counter: 0 }).animate({
    Counter: $('.counter2').text()
  }, {
    duration: 1500,
    easing: 'swing',
    step: function() {
      $('.counter2').text(Math.ceil(this.Counter));
    }
  });

  $({ Counter: 0 }).animate({
    Counter: $('.counter3').text()
  }, {
    duration: 2000,
    easing: 'swing',
    step: function() {
      $('.counter3').text(Math.ceil(this.Counter));
    }
  });

  $({ Counter: 0 }).animate({
    Counter: $('.counter4').text()
  }, {
    duration: 2000,
    easing: 'swing',
    step: function() {
      $('.counter4').text(Math.ceil(this.Counter));
    }
  });

  $({ Counter: 0 }).animate({
    Counter: $('.counter5').text()
  }, {
    duration: 2000,
    easing: 'swing',
    step: function() {
      $('.counter5').text(Math.ceil(this.Counter));
    }
  });



