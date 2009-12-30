/**
 * 功能:输入提示(ver0.1).
 * 
 * 服务器端数据要求返回JSON数据.数据结构如下
 * {'has_previous': false,
 *  'has_next': false,
 *  'page_number' : 1,
 *  'num_pages' : 1,
 *  'object_list': [['110','匪警'],['119','匪警'],['120','急救']]}
 *  或
 * {'has_previous': false,
 *  'has_next': false,
 *  'page_number' : 1,
 *  'num_pages' : 1,
 *  'object_list': ['110','119','120']}
 *
 * 缺省情况下object_list数组[0]作为返回值,放入输入框中,
 * 如果在构造函数中指定了decided_handler,
 * 那么选中的数据将以一维数组的形式出入decided_handler.
 * 
 * 具有分页功能,备选数据多页时,可以分页,
 * home[首页],end[末页],pageup[上翻页],pagedown[下翻页]会生效
 * 
 * 
 * @author 2009.6 yu.peng
 * 
 * 欢迎应用于无偿用途传播,并请勿移除版权声明.
 */


function addstyle(C,R){
  var stylesheets = document.styleSheets;
  if(!stylesheets||stylesheets.length<=0){
    var style = document.createElement("STYLE");
    style.type="text/css";
    var head = document.getElementsByTagName("HEAD")[0];
    head.appendChild(style)
  }
  stylesheets = document.styleSheets;
  stylesheets = stylesheets[stylesheets.length-1];
  if(Prototype.Browser.IE){
    stylesheets.addRule(C,R)
  }else{
    stylesheets.insertRule(C+" { "+R+" }",stylesheets.cssRules.length)
  }
}

addstyle("#suggest_div","border:1px solid #817F82;position:absolute;float:left;display:table");
addstyle("#suggest_div table","width:100%;background:#fff;cursor:default;font-size: 12px");
addstyle("#suggest_div td","white-space:nowrap;");
addstyle("#suggest_div .mo","background-color:#36c;color:#fff");
addstyle("#suggest_div .ml","background-color:#fff;color:#000");

// addstyle(".msgiframe","display:none; position:absolute;");

Suggest = Class.create({
  initialize: function(filed, request_url, decided_handler) {
    var pointer  = this;
    this.interval = null;
    this.timeout  = 0;
    this.div      = null;
    this.table    = null;
    this.pageup_handler = null;
    this.pagedown_handler = null;
    this.home_handler = null;
    this.end_handler = null;
    this.iframe   = null;    // 用于遮挡IE中的<select>
    this.selectedIndex = -1;

    this.input    = $(filed);
    this.input.setAttribute("autocomplete", 'off');
    this.request_url = request_url;
    this.decided_handler = decided_handler;
    // 监视鼠标是否移出该控件,当移出时,清空选择列表
    this.doc_md_handler   = function(e) { if (pointer.outside(e)) { pointer.close() } };
    this.win_blur_handler = function(e) { pointer.close() };
    // 输入框键盘按下时
    Event.observe(this.input, 'keydown', function(e){ pointer.onKeyDown(e) });
    // 输入框焦点移开下时
    Event.observe(this.input, 'blur', function(e){ pointer.close() });
    // 这个事件发生在控件无效之前,可以屏蔽在table中的文本选择(IE)
    Event.observe(this.input, 'beforedeactivate', function(e){
      return pointer.beforedeactivate(e);
    });
  },
  outside : function(e) {
    if (this.div) {
      var input_offsets = Position.positionedOffset(this.input);
      var div_offsets = Position.positionedOffset(this.div);
      if ((e.pointerX()<=div_offsets[0] || 
           e.pointerX()>=div_offsets[0] + this.div.getWidth() || 
           e.pointerY()<=div_offsets[1] || 
           e.pointerY()>=div_offsets[1]+this.div.getHeight())       &&
          (e.pointerX()<=input_offsets[0] || 
           e.pointerX()>=input_offsets[0] + this.input.getWidth() || 
           e.pointerY()<=input_offsets[1] || 
           e.pointerY()>=input_offsets[1]+this.input.getHeight()) ) {
        return true;
      } else {
        return false;
      }
    }
    return true;
  },
  beforedeactivate : function(e) {
    if (this.div) {
      e.stopPropagation();
      e.preventDefault();
      return false;
    }
  },

  onKeyDown : function(e) {
    var key = (!e) ? event.keyCode : e.keyCode;
    var ckey = (!e) ? event.ctrlKey : e.ctrlKey;
    switch(key){
      case 9:              // tab
      case 27:             // esc
        this.close();
        break;
      case 13:             // enter
        if (this.div) {
          if (this.selectedIndex==-1) {
            this.close();
          } else {
            this.decided();
          }
          e.stopPropagation();
          e.preventDefault();
          return false;
        }
        break;
      case 33:                            //pageup    上翻页
        if (this.div) {
          if (this.pageup_handler) {
            this.pageup_handler();
          }
          e.stopPropagation();
          e.preventDefault();
          return false;
        }
        break;
      case 34:                            //pagedown  下翻页
        if (this.div) {
          if (this.pagedown_handler) {
            this.pagedown_handler();
          }
          e.stopPropagation();
          e.preventDefault();
          return false;
        }
        break;
      case 35:                            //end  末尾页
        if (this.div) {
          if (this.end_handler) {
            this.end_handler();
          }
          e.stopPropagation();
          e.preventDefault();
          return false;
        }
        break;
      case 36:                            //home  首页
        if (this.div) {
          if (this.home_handler) {
            this.home_handler();
          }
          e.stopPropagation();
          e.preventDefault();
          return false;
        }
        break;
      case 38:                            //up    方向键上
        this.move('up');
        break;
      case 40:                            //down  方向键下
        this.move('down');
        break;
      default:                            // 需要确定一个范围
        if ((key>=48 && key<=111) ||      // 
            (key>=187) ||                 // 
            (key==8) ||                   // 退格
            (key==46)                     // Delete
            ) {
          if (!this.interval) {
            this.observing();
          }
        }
        break;
    }
  },
  observing : function() {
    var pointer = this;
    // pointer.buffer = null;    
    // pointer.buffer1 = null;   
    // pointer.selected = null;  
    this.interval = setInterval(function() {
      var req_data = pointer.input.value;
      if (req_data==pointer.buffer &&
          req_data!="" &&
          req_data!=pointer.buffer1 && 
          req_data!=pointer.selected) {
        if(pointer.timeout==0){
          pointer.timeout = setTimeout( function() {
                                          pointer.sendRequest(req_data);
                                        }, 100);
        }
      } else {
        clearTimeout(pointer.timeout);
        pointer.timeout = 0;
        pointer.buffer = req_data;
        if(req_data==""){
          pointer.close();
        }
        if(pointer.buffer1!=pointer.input.value){
          pointer.buffer1 = "";
        }
      }
    }, 100);
  },
  sendRequest : function(req_data, page_number) {
    var pointer = this;
    pointer.reflect(-1);
    if (this.request_url) {
      new Ajax.Request(this.request_url,
          {method: "get",
           requestHeaders: {RequestType: "ajax"},
           parameters: {req_data: req_data, page :(page_number ? page_number : 1)},
           asynchronous: false,
           onCreate:function(){},
           onSuccess:function(r){
             if (pointer.timeout!=0) {
               var json_data = r.responseJSON;
               if (json_data.object_list.length==0) {
                 pointer.hide();
               } else {
                 pointer.show(json_data);
               }
             }
          },
          onFailure:function(){}
         });
    }
  },
  move : function(direct) {
    if (this.div) {
      var row_size = this.table.rows.length-1;
      if  (direct=='up') {
        if (this.selectedIndex==-1) {
          this.reflect(row_size - 1);
        }else if (this.selectedIndex==0) {
          this.reflect(-1);
        } else {
          this.reflect(this.selectedIndex - 1);
        }
      } else {
        if (this.selectedIndex+1>=row_size) {
          this.reflect(-1);
        } else {
          this.reflect(this.selectedIndex + 1);
        }
      }
    }
  },
  reflect : function(idx) {
    if (this.selectedIndex!=-1) { this.table.rows[this.selectedIndex].className = "ml"; }
    this.selectedIndex = idx;
    if (this.selectedIndex!=-1) { this.table.rows[this.selectedIndex].className = "mo"; }
  },
  decided : function() {
    var ret = [];
    this.table.rows[this.selectedIndex].childElements().each(function(cell) {
      ret.push(cell.innerHTML);        // firefox 不支持innerText
    });
//    for (var i=0,cells=this.table.rows[this.selectedIndex].cells;i<cells.length;i++) {
//      ret.push(cells[i].innerHTML);   // firefox 不支持innerText
//    }
    this.input.value = ret[0]; 
    if (this.decided_handler) {    // 选中之后回调
      this.decided_handler(ret);
    }
    this.close();
  },
  tr_mousedown : function(e){
    e.stopPropagation();
    e.preventDefault();
    return false;
  },
  tr_mouseover_fun : function(idx) {
    var pointer = this;
    return function(e) {
      pointer.reflect(idx);
    };
  },
  tr_click_fun : function(idx){
    var pointer = this;
    return function(e) {
      pointer.reflect(idx);
      pointer.decided();
    };
  },
  show : function(data_hash){   // 使用table作为选择列表, 参考百度
    var pointer = this;
    // 创建div
    if (!this.div) {
      this.div = new Element("div");
      this.div.setAttribute('id','suggest_div');
      this.div.style.width = this.input.offsetWidth+'px';
      this.div.style.visibility = 'hidden';
      //this.input.parentNode.insertBefore(this.div, this.input);
      document.body.appendChild(this.div);
      // 先建立好后再调整位置
      var input_offsets = this.input.positionedOffset();
      this.div.style.top = (input_offsets.top + this.input.offsetHeight) + 'px';
      this.div.style.left = input_offsets.left + 'px';
      this.div.style.visibility = 'visible';

      // 当创建好图层时,监视鼠标是否移出该控件
      Event.observe(document, 'mousedown', this.doc_md_handler);
      Event.observe(window,   'blur',      this.win_blur_handler);

      if (Prototype.Browser.IE){
        this.iframe = new Element("iframe", {"style": "position:absolute;filter:progid:DXImageTransform.Microsoft.Alpha(opacity=0);"});
        this.iframe.src = "javascript:false";   // https时不弹出安全提示
        this.iframe.style.top = this.div.style.top;
        this.iframe.style.left = this.div.style.left;
        this.div.parentNode.insertBefore(this.iframe, this.div)
      }
    } else {
      this.table.remove();
    }
    this.table = new Element("table");
    this.table.cellSpacing=0;
    this.table.cellPadding=2;
    var tbody = new Element("tbody");
    var col_size = 1;
    this.table.appendChild(tbody);
    var object_list = data_hash.object_list;
    for(var i=0, m=object_list.length;i<m;i++){
      var row = tbody.insertRow(-1);
      Event.observe(row, 'mouseover', this.tr_mouseover_fun(i));
      Event.observe(row, 'mouseout',  function(e) { pointer.reflect(-1); });
      Event.observe(row, 'mousedown', function(e) { pointer.tr_mousedown(e) } );
      Event.observe(row, 'click',     this.tr_click_fun(i) );
      var record = object_list[i];
      if (Object.isArray(record)) {
        col_size = record.length;
        for (var i1=0, m1=col_size;i1<m1;i1++) {
          var cell = row.insertCell(-1);
          cell.innerHTML = record[i1].replace(/&/g,"&amp;")
          if (i1!=0) { cell.style.display = "none"; }             // 第二列以后的数据作为返回值,不予显示
        }
      } else {
        var cell = row.insertCell(-1);
        cell.innerHTML = record.replace(/&/g,"&amp;")
      }
    }
    // 末尾行
    var lastRow = tbody.insertRow(-1);
    Event.observe(lastRow, 'mousedown', function(e){ pointer.tr_mousedown(e) });
    var lastRowCell = lastRow.insertCell(-1);
    lastRowCell.style.textAlign = "right";
    lastRowCell.colSpan = col_size;
    
    
    
    // 上翻页是否可用
    if (data_hash.has_previous) {
      var previous_link = new Element("a");
      previous_link.href = "javascript:void(0)";
      previous_link.innerHTML = "上一页";
      this.home_handler = function(e){ pointer.sendRequest(pointer.input.value, 1) };
      this.pageup_handler = function(e){ pointer.sendRequest(pointer.input.value, data_hash.page_number-1) };
      Event.observe(previous_link, 'click', this.pageup_handler );
      lastRowCell.appendChild(previous_link);
      lastRowCell.appendChild(document.createTextNode(' '));
    } else {
      this.home_handler = null;
      this.pageup_handler = null;
    }
    // 下翻页是否可用
    if (data_hash.has_next) {
      var next_link = new Element("a");
      next_link.href = "javascript:void(0)";
      next_link.innerHTML = "下一页";
      this.end_handler = function(e){ pointer.sendRequest(pointer.input.value, data_hash.num_pages) };
      this.pagedown_handler = function(e){ pointer.sendRequest(pointer.input.value, data_hash.page_number+1) };
      Event.observe(next_link, 'click',  this.pagedown_handler );
      lastRowCell.appendChild(next_link);
      lastRowCell.appendChild(document.createTextNode(' '));
    } else {
      this.end_handler = null;
      this.pagedown_handler = null;
    }
    
    // [关闭]按钮
    var close_link = new Element("a");
    close_link.href = "javascript:void(0)";
    close_link.innerHTML = "关闭";
    Event.observe(close_link, 'click',  function(e){ pointer.close() } );
    lastRowCell.appendChild(close_link);
    
    this.div.appendChild(this.table);
    if (this.iframe!=null){
      this.iframe.style.width = this.div.offsetWidth + 'px';
      this.iframe.style.height = this.div.offsetHeight + 'px';
    }
  },
  hide : function() {
    this.reflect(-1);
    if (this.div) {
        this.div.remove();
        this.div = null;
        if (this.table) { this.table = null }
        if (this.pageup_handler) { this.pageup_handler = null }
        if (this.pagedown_handler) { this.pagedown_handler = null }
        if (this.home_handler) { this.home_handler = null }
        if (this.end_handler) { this.end_handler = null }
        Event.stopObserving(document, 'mousedown', this.doc_md_handler);    /* 图层关闭后移除监视 */
        Event.stopObserving(window,   'blur',      this.win_blur_handler);  /* 图层关闭后移除监视 */
        if (this.iframe) { this.iframe.remove(); this.iframe = null }
      }
  },
  close : function(){
    if (this.interval) { clearInterval(this.interval);this.interval = null }
    if (this.timeout!=0) { clearTimeout(this.timeout);this.timeout = 0 }
    this.hide();
  }
});

