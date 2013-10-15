// A simple users table
Splunk.Module.GetUsers = $.klass(Splunk.Module.DispatchingModule, {

    /*
     * overriding initialize to set up references and event handlers.
     */
    initialize: function($super, container) {
        $super(container);

        this.logger = Splunk.Logger.getLogger("Splunk.Module.GetUsers");
        this.resultsContainer = this.container;

    
    },

    onJobProgress: function (event) {
        this.getResults();
    },

    onJobDone: function (event) {
        this.getResults();
    },

    getResultParams: function($super) {
        var params = $super();
        var context = this.getContext();
        var search = context.get("search");
        var sid = search.job.getSearchId();

        if (!sid) this.logger.error(this.moduleType, "Assertion Failed.");

        params.sid = sid;
        return params;
    },

    renderResults: function($super, htmlFragment) {
        if (!htmlFragment) {
            this.resultsContainer.html('No content available.');
            return;
        }
        this.resultsContainer.html(htmlFragment);
    }

})

