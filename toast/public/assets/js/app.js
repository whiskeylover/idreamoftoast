/////////
// Models
/////////


// Dream
var Dream = Backbone.Model.extend
(
	{ 
		defaults: { count: 1 },
		
		initialize: function()
		{
			//alert(this.get('name'))
		}
	}
);


// DreamList
var DreamList = Backbone.Collection.extend
(
	{ 
		model: Dream,
		initialize: function()
		{
			//this.url = "http://127.0.0.1:5000/dreams/top";
			//this.fetch
			//(
			//	{
        	//		success: function () 
        	//		{
        	//			//alert(user.toJSON());
        	//			alert("yay");
        	 //       }
        	//   }
        	//);
			
		}
	}
);


////////
// Views
////////

// Dream
var DreamView = Backbone.View.extend
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


// DreamList
var DreamListView = Backbone.View.extend
(
	{ 
		//el: $('#populardreams'), // attaches `this.el` to an existing element.
		
		initialize: function(options)
		{
			var dreams = options["dreams"];
			this.collection = new DreamList(dreams);
			_.bindAll(this, 'render'); // fixes loss of context for 'this' within methods
			this.render(); // not all views are self-rendering. This one is.
		},
		
		render: function()
		{
			//$(this.el).append("<ul> <li>hello world</li> </ul>");
			var that = this;
			var i = 0;
			_.each(
				this.collection.models, 
				function (item) 
				{
					//if(i % 4 == 0)
					//{
					//	$(this.el).append("<div class=\"row-fluid\">");
					//}
					//$(that.el).append(item.render().el);
					that.renderDream(item);
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
		
		renderDream: function(item) 
		{
			var dreamView = new DreamView
			(
				{ model: item }
			);
			//$(this.el).append("<ul> <li>hello world</li> </ul>");
			$(this.el).append(dreamView.render().el);
			//$(this.el).append(item.get('name'));
		}
	}
);


(function($)
{
	var dreams = 
			[
				{ name: "Example 1", count: "100" },
				{ name: "Example 2", count: "75" },
				{ name: "Example 3", count: "65" },
				{ name: "Example 4", count: "55" },
				{ name: "Example 5", count: "45" },
				{ name: "Example 6", count: "40" },
				{ name: "Example 7", count: "35" },
				{ name: "Example 8", count: "25" }
			];
			
	var dreamListView = new DreamListView({dreams: dreams, el: "#populardreams", url: "http://127.0.0.1:5000/dreams/top"});      
})(jQuery);


