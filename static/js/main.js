(function(){


    var ModalView = Backbone.View.extend({

        initialize: function() {
            this.overlay = this.el.find('.overlay');
            this.content = this.el.find('.modal');
        }
    });

    ModalView.extend = function(child) {
        var view = Backbone.View.extend.apply(this, arguments);
        view.prototype.events = _.extend({}, this.prototype.events, child.events);
        return view;
    };

    var addQuestionModal = new (ModalView.extend({
        id: 'addQuestionModal',

        events: {
            'click .ico-close': 'close'
        },

        initialize: function() {
            console.log(this.$el);
            this.questionTextarea = this.$el.find('textarea');
        },

        render: function() {
            $(this.questionTextarea).expanding();
        },

        close: function() {
            this.$el.hide();
        }

    }))();

    var $addOverlay = $("#addQuestionOverlay"),
        $addQuestionModal = $("#addQuestionModal"),
        $addQuestionText = $("addQuestionText"),
        $addQuestionTags = $("addQuestionTags"),
        $addQuestBtn = $("#addQuestBtn");

    $addQuestBtn.on("click", function(e) {
        //$addOverlay.show();
        //$addQuestionModal.show();
        //$addQuestionModal.find('textarea').expanding();
        console.log(addQuestionModal.$el);
        addQuestionModal.$el.css('display', 'block');
    });

/*    $('.ico-close').on('click', function(e) {
        $(this).parent().hide();
        $(this).parent().parent().hide();
    });

    $addQuestionText.find('.btn').on('click', function(){
        $addQuestionText.hide();
        $addQuestionTags.show();
    });*/

})();