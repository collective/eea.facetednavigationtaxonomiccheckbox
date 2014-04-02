(function(jQuery) {
jQuery.fn.collapsible = function(settings){
  var self = this;
  var options = {
    maxitems: 0,
    elements: 'li',
  };
  self.colapsed = true;

  self.handle_refresh = function(){
    jQuery(self.elements, self).removeClass("hidden");
    self.less.addClass("hidden");
    self.more.addClass("hidden");
    if(!self.maxitems){
      return;
    }

    if(self.elements.length < self.maxitems){
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
      return;
    }
    self.elements.each(function(index){
      if(index < self.maxitems){
        jQuery(this).removeClass("hidden");
      }else{
        jQuery(this).addClass("hidden");
      }
    });
  };

  self.handle_expand=function(){
    self.colapsed = false;
    self.handle_refresh();
  };

  self.handle_colapse= function(){
    self.colapsed = true;
    self.handle_refresh();
  };

  // initialize
  self.initialize= function(){
    self.more = jQuery("> .faceted-checkbox-more .more", self);
    self.less = jQuery("> .faceted-checkbox-more .less", self);
    self.elements = jQuery(options.elements, self);
    self.maxitems = options.maxitems;

    self.more.click(function(){
      self.handle_expand();
      return false;
    });
    self.less.click(function(){
      self.handle_colapse();
      return false;
    });

  };

  if(settings){
    jQuery.extend(options, settings);
  }
  self.initialize();
  return this;
  };
})(jQuery);
