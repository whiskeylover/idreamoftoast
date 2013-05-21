$(function() {

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
            'dreams': 'dreams',
            'dreams/:dream': 'getDream',
            'about': 'about'
        }
    });

    // Views
    var IndexView = Backbone.View.extend({
        el: '#hook',
        template: '#tmpl_index',
        events: {
            'click button#btn-submit': 'addDream'
        },
        initialize: function() {
            _.bindAll(this, 'render', 'addDream');
            var self = this;
        },
        render: function(tmpl, data) {
            var self = this;
            var template = _.template($(self.template).html(),
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

            // This is NOT the ideal way to do this in Backbone. This
            // should be updated in the future, but works for now!
            $.getJSON('/dreams/add/' + dream, function(result) {
                router.navigate('dreams/' + dream, {trigger: true});
            });
        }
    });

    DreamsView = Backbone.View.extend({
        el: '#hook',
        template: '#tmpl_dreams',
        initialize: function() {
            _.bindAll(this, 'render', 'load', 'getDream');
            var self = this;

            self.dream = new Dream();
            self.topDreams = new TopDreams();
            self.recentDreams = new RecentDreams();

            // dependencies
            self.topDreams.on('sync', self.render);
            self.recentDreams.on('sync', self.render);
        },
        render: function() {
            var self = this;
            var template = _.template($(self.template).html(),
                                      {dream: self.dream,
                                       topDreams: self.topDreams.models,
                                       recentDreams: self.recentDreams.models});
            this.$el.html( template );
            return this;
        },
        load: function() {
            var self = this;
            // Go fetch some dreams!
            self.topDreams.fetch();
            self.recentDreams.fetch();
        },
        getDream: function(dream) {
            var self = this;
            // This is NOT the ideal way to do this in Backbone. This
            // should be updated in the future, but works for now!
            $.getJSON('/dreams/get/' + dream, function(result) {
                self.dream = new Dream(result);
                self.render();
            });
        }
    });

    AboutView = Backbone.View.extend({
        el: '#hook',
        template: '#tmpl_about',
        initialize: function() {
            _.bindAll(this, 'render');
            var self = this;
        },
        render: function() {
            var self = this;
            var template = _.template($(self.template).html(),
                                      {});
            this.$el.html( template );
            return this;
        }
    });

    // Instantiations
    var indexView = new IndexView();
    var dreamsView = new DreamsView();
    var aboutView = new AboutView();
    var router = new Router();

    // Routes
    router.on('route:index', function() {
        console.log('Load the index page!');
        indexView.render();
    });

    router.on('route:dreams', function() {
        console.log('Load the dreams page!');
        dreamsView.load();
    });

    router.on('route:getDream', function(dream) {
        console.log('Get a dream!');
        dreamsView.load();
        dreamsView.getDream(dream);
    });

    router.on('route:about', function(dream) {
        console.log('Load the about page!');
        aboutView.render();
    });

    // Let's get this party started!
    Backbone.history.start();
});
