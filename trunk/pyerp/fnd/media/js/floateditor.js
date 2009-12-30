/**
 * 功能:...
 * 
 * 
 * 
 * @author 2009.8 yu.peng
 * 
 * 欢迎应用于无偿用途传播,并请勿移除版权声明.
 */


FloatEditor = Class.create({
  initialize: function(filed, handlers) {
    this.input = $(filed);
    this.handlers = handlers;
    var pointer = this;
    this.input.oldvalue = this.input.value;
    Event.observe(this.input, "keydown", function(e){ return pointer.onKeyDown(e) });
    // 当创建好图层时,监视鼠标是否移出该控件
    Event.observe(this.input, "focus", function(e){ pointer.input.select() });
    Event.observe(this.input, "blur", function(e){ pointer.decided(0) });
    Event.observe(this.input, "click", function(e){ pointer.input.select() });   // for ff
    // this.doc_md_handler   = function(e) { if (pointer.outside(e)) { pointer.decided(0) } };
    // Event.observe(document, 'mousedown', pointer.doc_md_handler);
  },
  outside : function(e) {
    var input_offsets = Position.positionedOffset(this.input);
    if ((e.pointerX()<=input_offsets[0] || 
         e.pointerX()>=input_offsets[0] + this.input.getWidth() || 
         e.pointerY()<=input_offsets[1] || 
         e.pointerY()>=input_offsets[1]+this.input.getHeight()) ) {
      return true;
    } else {
      return false;
    }
    return true;
  },
  onKeyDown: function(e) {
    var key = (!e) ? event.keyCode : e.keyCode;
    var ckey = (!e) ? event.ctrlKey : e.ctrlKey;
    var sKey = (!e) ? event.shiftKey : e.shiftKey;
    var pointer = this;
    switch(key){
      case 9:              // tab
      case 13:             // enter
        if (sKey) {
          pointer.decided(-1);   // 焦点向前移动
        } else {
          pointer.decided(1);    // 焦点向后移动
        }
        e.stopPropagation();
        e.preventDefault();
        return false;
        break;
      case 27:                   // esc
        this.input.value = this.input.oldvalue;
        this.input.select();
        e.stopPropagation();
        e.preventDefault();
        return false;
        break; 
    }
  },
  decided : function(next) {
    // Event.stopObserving(document, 'mousedown', this.doc_md_handler);    /* 图层关闭后移除监视 */
    var changed = this.oldvalue!=this.input.value;
    if (this.handlers.ondecid) {
      this.handlers.ondecid(next);
    }
  }
});

