$(function() {

    // Magic underscore settings to allow underscore templates to play
    // nicely with Rails ERB templates!
    _.templateSettings = {
        interpolate: /\{\{\=(.+?)\}\}/g,
        evaluate: /\{\{(.+?)\}\}/g
    };

////////
// Views
////////

// Dream mini view
var DreamMiniView = Backbone.View.extend
(
	{
		tagName: "div",
		className: "span3 center",

		template: $("#dreamTemplate").html(),

		render: function ()
		{
			var variables = {name: this.model.get('name'), count: this.model.get('count')};
			var tmpl = _.template(this.template);
			//this.$el.html(tmpl(this.model.toJSON())); // <-- fails here
			//this.$el.html(tmpl(this.model.toJSON())); // <-- fails here
			$(this.el).html(tmpl(this.model.toJSON())); // <-- this worked
			return this;
		}
	}
);


var DreamView = Backbone.View.extend
(
	{
		el: "#thedream",
		template: $("#theDreamTemplate").html(),
		model: Dream,

		initialize: function(options)
		{
			var url = '/dreams/get/' + options['name'];
			this.model = new Dream([], {url: url});
			this.listenTo( this.model, 'sync', this.render ); // Trigger render when model has been loaded

			this.model.fetch
			();
		},

		render: function()
		{
			//alert('here');
			var tmpl = _.template(this.template);
			//alert(this.model.toJSON());
			$(this.el).html(tmpl(this.model.toJSON()));
		}
	}
);


// DreamList
var DreamListView = Backbone.View.extend
(
	{
		//el: $('#populardreams'), // attaches `this.el` to an existing element.

		initialize: function(options)
		{
			var url = options["url"];
			this.collection = new DreamList([], {url: url});
			this.collection.fetch({type: "GET", reset: true});
			_.bindAll(this, 'render'); // fixes loss of context for 'this' within methods
			//this.render(); // not all views are self-rendering. This one is.

			this.listenToOnce( this.collection, 'reset', this.render ); // Trigger render when list has been loaded
		},

		render: function()
		{
			var that = this;
			var i = 0;
			var div_row_fluid;
			//alert(this.collection.toJSON());
			_.each(
				this.collection.models,
				function (item)
				{
					if(i % 4 == 0)
					{
						div_row_fluid = $('<div class=\"row-fluid\"></div>');
						$(this.el).append(div_row_fluid);
						//$(this.el).append("<div class=\"row-fluid\">");
					}
					//$(that.el).append(item.render().el);
					that.renderDream(div_row_fluid, item);
					//if(i % 4 == 0)
					//{
					//	$(this.el).append("</div>");
					//}
					//$(that.el).append(item.render().el);
					i++;

				},
				this
			);
		},

		renderDream: function(div_row_fluid, item)
		{
			var dreamMiniView = new DreamMiniView
			(
				{
					model: item
				}
			);
			//$(this.el).append(dreamMiniView.render().el);
			div_row_fluid.append(dreamMiniView.render().el);
		}
	}
);

    // Models & Collections
    var Dream = Backbone.Model.extend();

    var TopDreams = Backbone.Collection.extend({
        model: Dream,
        url: '/dreams/top',
        parse: function(response) {
            return response;
        }
    });

    var RecentDreams = Backbone.Collection.extend({
        model: Dream,
        url: '/dreams/recent',
        parse: function(response) {
            return response;
        }
    });

    // Router
    var Router = Backbone.Router.extend({
        routes: {
            '': 'index',
            'dreams': 'dreams'
        }
    });

    // Views
    var IndexView = Backbone.View.extend({
        el: '#hook',
        events: {
            'click button#btn-submit': 'addDream'
        },
        initialize: function() {
            _.bindAll(this, 'render', 'addDream');
            var self = this;
        },
        render: function(tmpl, data) {
            var self = this;
            var template = _.template($("#tmpl_index").html(),
                                      {});
            this.$el.html( template );
            // Hide the spinner after the template renders.
            $('#spinner', self.el).hide();
            return this;
        },
        addDream: function() {
            console.log('Add dream!');
            var self = this;
            var dream = $('#dream', self.el).val();

            $('#spinner', self.el).show();

            // This should really be a model call.
            $.getJSON('/dreams/add/' + dream, function(result) {
                router.navigate('dreams', {trigger: true});
            });
        }
    });

    DreamsView = Backbone.View.extend({
        el: '#hook',
        template: '#tmpl_dreams',
        initialize: function() {
            _.bindAll(this, 'render');
            var self = this;

            self.topDreams = new TopDreams();
            self.recentDreams = new RecentDreams();
            self.topDreams.fetch();
            self.recentDreams.fetch();

            // dependencies
            self.topDreams.on('sync', self.render);
            self.recentDreams.on('sync', self.render);
        },
        render: function() {
            var self = this;
            var template = _.template($(self.template).html(),
                                      {topDreams: self.topDreams.models,
                                       recentDreams: self.recentDreams.models});
            this.$el.html( template );
            return this;
        }
    });

    // Instantiations
    var indexView = new IndexView();
    var dreamsView = new DreamsView();
    var router = new Router();

    router.on('route:index', function() {
        console.log('Load the index page!');
        indexView.render();
    });

    router.on('route:dreams', function() {
        console.log('Load the dreams page!');
        dreamsView.render();
    });

    // Let's get this party started!
    Backbone.history.start();
});
