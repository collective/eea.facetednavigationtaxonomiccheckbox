(function(jQuery) {
jQuery.fn.collapsible = function(settings){
  var self = this;
  var options = {
    maxitems: 0,
    elements: 'li',
  };
  var events ={
      refresh: 'widget-refresh',
      expand: 'widget-expand',
      colapse: 'widget-colapse'
  };
  self.colapsed = true;

  self.handle_refresh = function(){
    console.log("handle_refresh");
    jQuery(options.elements, self).removeClass("hidden");
    self.less.addClass("hidden");
    self.more.addClass("hidden");
    if(!self.maxitems){
      return;
    }
    var elements = jQuery(options.elements, self);
    if(elements.length < self.maxitems){
      return;
    }

    if(self.colapsed){
      self.less.addClass("hidden");
      self.more.removeClass("hidden");
    }else{
      self.less.removeClass("hidden");
      self.more.addClass("hidden");
    }

    if(!self.colapsed){
      console.log("COLLAPSED!");
      return;
    }
    elements.each(function(index){

      if(index < self.maxitems){
        jQuery(this).removeClass("hidden");
      }else{
        jQuery(this).addClass("hidden");
      }
    });
  };

  self.handle_expand=function(){
    self.colapsed = false;
    self.trigger(events.refresh);
  };

  self.handle_colapse= function(){
    self.colapsed = true;
    self.trigger(events.refresh);
  };

  // initialize
  self.initialize= function(){
    self.more = jQuery("> .faceted-checkbox-more .more", self);
    self.less = jQuery("> .faceted-checkbox-more .less", self);
    self.maxitems = parseInt(options.maxitems, 10);

    self.bind(events.refresh, self.handle_refresh);
    self.bind(events.expand, self.handle_expand);
    self.bind(events.colapse, self.handle_colapse);

    self.more.click(function(){
      self.trigger(events.expand);
      return false;
    });
    self.less.click(function(){
      self.trigger(events.colapse);
      return false;
    });
    // self.colapsed = true;
    self.handle_refresh();
  };

  if(settings){
    jQuery.extend(options, settings);
  }
  self.initialize();
  return this;
  };
})(jQuery);
