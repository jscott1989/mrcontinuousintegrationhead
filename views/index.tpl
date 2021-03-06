<!DOCTYPE html>
<html>
  <head>
    <title>{{name}} Status</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css">
  	<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-theme.min.css">
    <style>
      ul.log {
        height: 200px;
        overflow: scroll;
      }

      .test-form button {
        margin-top: 10px;
        width: 150px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>{{name}}</h1>
      <div class="row">
        <div class="col-md-6">
          <h2>Configuration</h2>
          <form action="/config" method="POST" role="form" class="ajax form-horizontal">
            % for key, value in configuration.items():
              <div class="form-group">
                <label class="col-lg-2 control-label" for="{{key}}">{{key}}</label>
                <div class="col-lg-10">
                  <input type="text" name="{{key}}" value="{{value}}">
                </div>
              </div>
            % end
            <button class="btn btn-default" type="submit">Save changes</button>
          </form>
          <h2>Testing</h2>
          % for id, function in test_functions:
          <form action="/function/{{id}}" method="POST" class="ajax test-form">
            <button class="btn btn-default" type="submit">{{function}}</button>
          </form>
          % end
        </div>
        <div class="col-md-6">
          <h2>Log</h2>
          <ul class="log" data-bind="foreach: ordered_log">
            <li data-bind="text: $data"></li>
          </ul>
          <form action="/clear_log" method="POST" class="ajax">
            <button class="btn btn-default" type="submit">Clear Log</button>
          </form>
          <h2>Status</h2>
          <table data-bind="foreach: status">
            <tr>
              <td><strong data-bind="text: key"></strong></td>
              <td data-bind="html: value"></td>
          </table>
        </div>
      </div>

    </div>
    <script src="http://code.jquery.com/jquery.js"></script>
    <script src="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
    <script src="http://cdnjs.cloudflare.com/ajax/libs/knockout/2.3.0/knockout-min.js"></script>
    <script src="http://cdnjs.cloudflare.com/ajax/libs/knockout.mapping/2.3.5/knockout.mapping.js"></script>
    <script src="http://js.pusher.com/2.1/pusher.min.js" type="text/javascript"></script>
    <script src="http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.4.4/underscore-min.js"></script>
    <script>

      // Viewmodel stuff
      % import json
      % dumped_viewmodel = json.dumps(viewmodel)
      viewmodel = {}

      viewmodel = ko.mapping.fromJS({{!dumped_viewmodel}});

      viewmodel.ordered_log = ko.computed(function() {
        return _.clone(viewmodel.log()).reverse();
      })

      ko.applyBindings(viewmodel);

      // Pusher for live updates
      var pusher = new Pusher('2c0e2063352f3e58148f');
      var channel = pusher.subscribe('{{name}}');
      channel.bind('log', function(data) {
        viewmodel.log.push(data.logstring);
      });

      channel.bind('clear-log', function() {
        viewmodel.log.removeAll();
      });

      channel.bind('change-status', function(data) {
        // Find the correct status and update it
        var found_status = _.filter(viewmodel.status(), function(x) {
          return x.key() == data.key;
        });

        if (found_status.length > 0) {
          _.each(found_status, function(x) {
            x.value(data.value);
          });
        } else {
          viewmodel.status.push({key: ko.observable(data.key), value: ko.observable(data.value)});
        }
      });

      // Make forms ajax
      $('body').on('submit', 'form.ajax', function() {
        $this = $(this);
        $.post($this.attr('action'), $this.serialize());
        return false;
      });
    </script>
  </body>
</html>