/////////
// Models
/////////


// Dream
var Dream = Backbone.Model.extend
(
	{ 
		defaults: { count: 1 },
		
		//initialize: function()
		//{
		//	alert("Creating dream " + this.get('name'))
		//}
	}
);


// DreamList
var DreamList = Backbone.Collection.extend
(
	{ 
		model: Dream//,
		//url: "http://127.0.0.1:5000/dreams/top",
		//initialize: function()
		//{
			//alert("Collection url is " + this.url);
			/*this.fetch
			(
				{
					type: "GET",
        			success: function () 
        			{
						alert("yes");
           	       	},
        	       	error: function()
        	       	{
        	       		alert("Oh Noes");
        	       	}
        	   	}
        	);*/
			
		//}
	}
);


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
			var url = 'http://127.0.0.1:5000/dreams/get/' + options['name'];
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






