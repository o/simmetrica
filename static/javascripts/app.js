function App() {

  var ajaxHandlers = {};
  var domBuilders = {};
  var partialViews = {};
  var helpers = {};

  var series = null;
  var graph = null;
  var palette = null;
  var legend = null;
  
  var sizes = {
    'S': 250,
    'M': 550,
    'L': 850,
    'XL': 1150
  }

  ajaxHandlers.graph = function () {
    $.get('/graph', function (data) {
      domBuilders.renderGraphs(data);
    }).error(function () {
      domBuilders.renderError();
    });
  };

  domBuilders.renderGraphs = function (data) {
    $.each(data, function (index, section) {
      $('#loading').remove();
      $('#graphs').append(partialViews.graphSection(section));
      helpers.renderGraph(section);
    });
  };

  partialViews.graphSection = function (section) {
    return '<section class="graph-section" id="' + section.identifier + '"><h3 class="graph-title">' + section.title + '</h3><div class="graph-container"><div class="y-axis"></div><div class="graph"></div></div><div class="legend"></div></section>';
  };

  domBuilders.renderError = function () {
    $('#loading').remove();
    $('#errormessage').text('An error occured when loading graphs.');
  };

  helpers.renderGraph = function (section) {
    series = [];

    palette = new Rickshaw.Color.Palette({
      scheme: section.colorscheme
    });
    
    $.each(section.events, function (index, event) {
      series.push({
        data: event.data,
        color: palette.color(),
        name: event.title
      })
    });

    graph = new Rickshaw.Graph({
      element: document.querySelector('#' + section.identifier + ' .graph'),
      width: sizes[section.size],
      height: 300,
      series: series,
      renderer: section.type,
      interpolation: section.interpolation,
      offset: section.offset
    });

    legend = new Rickshaw.Graph.Legend({
      graph: graph,
      element: document.querySelector('#' + section.identifier + ' .legend')
    });

    new Rickshaw.Graph.Behavior.Series.Toggle({
      graph: graph,
      legend: legend
    });

    new Rickshaw.Graph.Behavior.Series.Order({
      graph: graph,
      legend: legend
    });

    new Rickshaw.Graph.Behavior.Series.Highlight({
      graph: graph,
      legend: legend
    });

    new Rickshaw.Graph.Axis.Time({
      graph: graph,
      timeFixture: new Rickshaw.Fixtures.Time.Local()
    });

    new Rickshaw.Graph.Axis.Y({
      graph: graph,
      element: document.querySelector('#' + section.identifier + ' .y-axis'),
      orientation: 'left',
      tickFormat: Rickshaw.Fixtures.Number.formatKMBT
    });

    new Rickshaw.Graph.HoverDetail( {
      graph: graph,
      xFormatter: function (x) {
        return new Date(x * 1000).toString();
      }
    });

    graph.render();
  };

  this.init = function () {
    ajaxHandlers.graph();
  };

}

$.ajaxSetup({
  cache: false,
  dataType: 'json'
});

var app = new App();
app.init();