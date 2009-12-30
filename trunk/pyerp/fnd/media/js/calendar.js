/**
 * 功能:日期输入.
 *
 * 使用方法:
 * 1. 这个方法会在输入框后创建一个按钮,按下可以打开"日期输入".
 *   <input type="text" id="date1" size="32" value="2009/08/02"/>
 *   <script>var date1 = new Calendar('date1');<script>
 * 
 * 2. 这个方法会在btn_date2上加上click事件,按下可以打开"日期输入".
 *   <input type="text" id="date2" size="32" value=""/><img id="btn_date2" src="/images/icon_calendar.gif" style="cursor:pointer"/>
 *   var date1 = new Calendar('date2', 'btn_date2');
 * 
 * 
 * 功能键:
 *    Home-上一年
 *    End-下一年
 *    PageUp-上一个月
 *    PageDown-下一个月
 *    Up-显示/隐藏日期输入
 *    Down-显示/隐藏日期输入
 * 
 * @author 2009.8 yu.peng
 * 
 * 欢迎应用于无偿用途传播,并请勿移除版权声明.
 */


addstyle("#calendar_div","border:1px solid #817F82;position:absolute;float:left;display:table");
addstyle("#calendar_div table","text-align: center;width:100%;border:0;background:#fff;cursor:default;font-size: 12px;");
addstyle("#calendar_div table td","white-space: nowrap;");
addstyle("#calendar_div table .footer","text-align: right;font-size: 12px;");

addstyle("#calendar_div .in_body","text-align: center;width:100%;border:1 solid #cccccc;font-size: 12px");
addstyle("#calendar_div .in_body .header","background-color: #efefef;");
addstyle("#calendar_div .in_body .weekend","color: red;");
addstyle("#calendar_div .in_body .weekday","color: #161616;");
addstyle("#calendar_div .in_body .not_this_month","color: #c0c0c0;");
addstyle("#calendar_div .in_body .this_month","color: #1d1d72;cursor:pointer;");
addstyle("#calendar_div .in_body td","color: #ffcc99;");
addstyle("#calendar_div .in_body .cell_weekend","background-color: #ffeeee;");
addstyle("#calendar_div .in_body .cell_weekday","background-color: #eeeeff;");
addstyle("#calendar_div .in_body .cell_today","background-color: #ffff99;");
addstyle("#calendar_div .in_body .cell_input","background-color: #ffcc99;");


Calendar = Class.create({
  weekDayStr: new Array( "日","一","二","三","四","五","六"),
  dateSeparator: "/",
  /**
   * 根据字符串取得日期,失败时返回系统日期.
   */
  parseDate: function (dateStr) {
    if (!dateStr) {
      return new Date();
    }
    var dateRegExp = new RegExp("^\\d{4}" + this.dateSeparator + "\\d{1,2}" + this.dateSeparator + "\\d{1,2}$");
    if (!dateRegExp.test(dateStr)) { 
        return new Date();
    }
    var year, month, day;
    var dateArray = dateStr.split(this.dateSeparator);
    year  = parseInt(dateArray[0], 10);
    month = parseInt(dateArray[1], 10);
    day   = parseInt(dateArray[2], 10);
    var di = new Date(year, month-1, day);
    if(di.getFullYear()==year && di.getMonth()==month-1 && di.getDate()==day) {
      return di;
    }
    return new Date();
  }, 
  /**
   * 取得某月的日期列表.
   * 
   * getDates(2007, 12).
   *     1     false       2007/11/25
   *     2-5   false       ...
   *     6     false       2007/11/30
   *     7     true        2007/12/01
   *     8-36  true        ...
   *     37    true        2007/12/31
   *     38    false       2008/01/01
   *     38-41 false       ...
   *     42    false       2008/01/05
   *
   * @param  year         
   * @param  month        
   */
  monthlyQueue: function(year, month) {
    var firstDateOfMonth = new Date(year, month-1, 1);
    var lastDateOfMonth = new Date(year, month, 0);
    var monthDates = [];
    var i;
    if (firstDateOfMonth.getDay()!=0) {
      for (i=1;i<=(firstDateOfMonth.getDay());i++) {
        var temp = [];
        temp.push(false);
        temp.push(new Date(year, month-1, i-firstDateOfMonth.getDay()));
        monthDates.push(temp);
      }
    }
    for (i=1;i<=lastDateOfMonth.getDate();i++) { 
        var temp = [];
        temp.push(true);
        temp.push(new Date(year, month-1, i));
        monthDates.push(temp);
    }
    if (lastDateOfMonth.getDay()!=6) {
      for (i=1;i<=(6-lastDateOfMonth.getDay());i++) {
        var temp = [];
        temp.push(false);
        temp.push(new Date(year, month-1, lastDateOfMonth.getDate()+i));
        monthDates.push(temp);
      }
    }
    return monthDates;
  },
  leftPad: function (str) {
    if (str) {
      if (str.length==1) {
        return "0" + str;
      } else {
        return str;
      }
    }
    return "";
  },
  initialize: function(filed, btn_toggle, decided_handler) {
    var pointer  = this;
    this.div      = null;
    this.pageup_handler = null;   // 上个月
    this.pagedown_handler = null; // 下个月
    this.home_handler = null;     // 上一年
    this.end_handler = null;      // 下一年
    
    this.iframe   = null;         // 用于遮挡IE中的<select>

    this.input    = $(filed);
    this.input.setAttribute("autocomplete", 'off');
    
    if ($(btn_toggle)) {
      this.btn_toggle = $(btn_toggle);
    } else {
      this.btn_toggle = new Element("input", {"type": "button", "value": "..."});
      this.input.parentNode.appendChild(this.btn_toggle);
    }
    this.btn_toggle.observe('click', function(e){ pointer.toggle(); pointer.input.focus(); pointer.input.select(); });

    this.decided_handler = decided_handler;
    // 监视鼠标是否移出该控件,当移出时,清空选择列表
    this.doc_md_handler   = function(e) { if (pointer.outside(e)) { pointer.close() } };
    this.win_blur_handler = function(e) { pointer.close() };
    // 输入框键盘按下时
    Event.observe(this.input, 'keydown', function(e){ pointer.onKeyDown(e) });
    // 这个事件发生在控件无效之前,可以屏蔽在table中的文本选择(IE)
    Event.observe(this.input, 'beforedeactivate', function(e){ return pointer.beforedeactivate(e); });
  },
  outside: function(e) {
    if (this.div) {
      var input_offsets = Position.positionedOffset(this.input);
      var div_offsets = Position.positionedOffset(this.div);
      var btn_offsets = Position.positionedOffset(this.btn_toggle);
      if ((e.pointerX()<=div_offsets[0] || 
           e.pointerX()>=div_offsets[0] + this.div.getWidth() || 
           e.pointerY()<=div_offsets[1] || 
           e.pointerY()>=div_offsets[1]+this.div.getHeight())       &&
          (e.pointerX()<=input_offsets[0] || 
           e.pointerX()>=input_offsets[0] + this.input.getWidth() || 
           e.pointerY()<=input_offsets[1] || 
           e.pointerY()>=input_offsets[1]+this.input.getHeight())       &&
          (e.pointerX()<=btn_offsets[0] || 
           e.pointerX()>=btn_offsets[0] + this.btn_toggle.getWidth() || 
           e.pointerY()<=btn_offsets[1] || 
           e.pointerY()>=btn_offsets[1]+this.btn_toggle.getHeight()) ) {
        return true;
      } else {
        return false;
      }
    }
    return true;
  },
  beforedeactivate: function(e) {
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
      case 33:                            // pageup    上翻页
        if (this.div) {
          if (this.pageup_handler) {
            this.pageup_handler();
          }
          e.stopPropagation();
          e.preventDefault();
          return false;
        }
        break;
      case 34:                            // pagedown  下翻页
        if (this.div) {
          if (this.pagedown_handler) {
            this.pagedown_handler();
          }
          e.stopPropagation();
          e.preventDefault();
          return false;
        }
        break;
      case 35:                              //end  末尾页
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
      case 40:                            //down  方向键下
          this.toggle();
        break;
    }
  },
  toggle: function() {
    if (this.div) {
      this.close();
    } else {
      this.show(this.parseDate(this.input.value));
    }
  },
  show: function(div_curr_date){   // 使用table作为选择列表
    var pointer = this;
    if (!this.div) {
      this.div = new Element("div");
      this.div.setAttribute('id','calendar_div');
      this.div.style.width = this.input.offsetWidth+'px';
      this.div.style.visibility = 'hidden';
      document.body.appendChild(this.div);
      // 先建立好后再调整位置
      var input_offsets = this.input.positionedOffset();
      this.div.style.top = (input_offsets.top + this.input.offsetHeight) + 'px';
      this.div.style.left = input_offsets.left + 'px';
      this.div.style.visibility = 'visible';
      // 当创建好图层时,监视鼠标是否移出该控件
      Event.observe(document, 'mousedown', this.doc_md_handler);
      Event.observe(window,   'blur',      this.win_blur_handler);
      if (Prototype.Browser.IE) {
        this.iframe = new Element("iframe", {"style": "position:absolute;filter:progid:DXImageTransform.Microsoft.Alpha(opacity=0);"});
        this.iframe.src = "javascript:false";   // https时不弹出安全提示
        this.iframe.style.top = this.div.style.top;
        this.iframe.style.left = this.div.style.left;
        this.div.parentNode.insertBefore(this.iframe, this.div)
      }
    } else {
      this.div.innerHTML = "";
    }

    var year = div_curr_date.getFullYear(), month = div_curr_date.getMonth() + 1, day = div_curr_date.getDate();
    var fromY = year - 5, toY   = year + 5;
    var i, j, index;
    var todayDate = new Date();
    var _table_0 = new Element("table");
    var _tbody_0 = new Element("tbody"); _table_0.appendChild(_tbody_0);

    // header
    var _header_tr = new Element("tr"); _tbody_0.appendChild(_header_tr); Event.observe(_header_tr, 'mousedown', function(e) { e.stopPropagation(); e.preventDefault(); return false; } );
    var _header_td = new Element("td"); _header_tr.appendChild(_header_td);
    var previous_m_link = new Element("a", {"href": "javascript:void(0)"}).update((month-1==0 ? 12 : month-1) + "月"); _header_td.appendChild(previous_m_link);
    this.pageup_handler = function(e){ pointer.show(new Date(year, month-2, 1)); };
    Event.observe(previous_m_link, 'click', this.pageup_handler );
    _header_td.appendChild(document.createTextNode(' '));
    _header_td.appendChild(new Element("b").update(year + "年" + pointer.leftPad(""+month) + "月 "));
    var next_m_link = new Element("a", {"href": "javascript:void(0)"}).update((month+1==13 ? 1 : month+1) + "月"); _header_td.appendChild(next_m_link);
    this.pagedown_handler = function(e){ pointer.show(new Date(year, month, 1)); };
    Event.observe(next_m_link, 'click',  this.pagedown_handler );

/*
    var _year_select = new Element("select", {"style": "font-size: 8px"});
    var _month_select = new Element("select", {"style": "font-size: 8px"});
    Event.observe(_year_select, 'change',  function(e) { pointer.show(new Date(parseInt(_year_select.value), parseInt(_month_select.value)-1, 1)); });
    Event.observe(_month_select, 'change',  function(e){ pointer.show(new Date(parseInt(_year_select.value), parseInt(_month_select.value)-1, 1)); });
    for ( var i = fromY; i <= toY; i++ ) {
      var _year_option;
      if( i == year ) {
        _year_option = new Element("option", {"selected": "true", "value":i }).update(i);
      } else {
        _year_option = new Element("option", {"value":i }).update(i);
      }
      _year_select.appendChild(_year_option);
    } 
    for ( var j = 1; j <= 12; j++ ) {
      var _month_option;
      if ( j == month ) {
        _month_option = new Element("option", {"selected": "true", "value":j }).update(j);
      } else {
        _month_option = new Element("option", {"value":j }).update(j);
      }
      _month_select.appendChild(_month_option);
    }
    _header_th.appendChild(_year_select);
    _header_th.appendChild(document.createTextNode('年'));
    _header_th.appendChild(_month_select);
    _header_th.appendChild(document.createTextNode('月'));
*/
    
    var _body_tr = new Element("tr"); _tbody_0.appendChild(_body_tr); Event.observe(_body_tr, 'mousedown', function(e) { e.stopPropagation(); e.preventDefault(); return false; } );
    var _body_td = new Element("td"); _body_tr.appendChild(_body_td);
    var _in_table = new Element("table", {"class": "in_body"}); _body_td.appendChild(_in_table);
    var _in_tbody = new Element("tbody"); _in_table.appendChild(_in_tbody);
    var _in_tr_1 = new Element("tr", {"class": "header"}); _in_tbody.appendChild(_in_tr_1); Event.observe(_in_tr_1, 'mousedown', function(e) { e.stopPropagation(); e.preventDefault(); return false; } );
    for (i=0;i<7;i++) {
      if (i==0||i==6) {
        var _in_td = new Element("td", {"class": "weekend"}).update(this.weekDayStr[i]); _in_tr_1.appendChild(_in_td);
      } else {
        var _in_td = new Element("td", {"class": "weekday"}).update(this.weekDayStr[i]); _in_tr_1.appendChild(_in_td);
      }
    }

    var monthDates = this.monthlyQueue(year, month);
    index = 0;
    var row_size = monthDates.length / 7;
    for (i=0;i<row_size;i++) {
      var _in_tr_2 = new Element("tr"); _in_tbody.appendChild(_in_tr_2); Event.observe(_in_tr_2, 'mousedown', function(e) { e.stopPropagation(); e.preventDefault(); return false; } );
      for (j=0;j<7;j++) {
        index = i * 7 + j;
        var lDate = monthDates[index][1];
        var _in_td_2 = new Element("td").update(lDate.getDate()); _in_tr_2.appendChild(_in_td_2);
        
        if (!monthDates[index][0]) {     // 不是这个月的日期
          _in_td_2.addClassName("not_this_month");
        } else {
          var input_date = this.parseDate(this.input.value);
          if (input_date && lDate.getFullYear()==input_date.getFullYear() 
              && lDate.getMonth()==input_date.getMonth()
              && lDate.getDate()==input_date.getDate()) {           // 与输入框中日期相同
            _in_td_2.addClassName("cell_input");
          } else if (lDate.getFullYear()==todayDate.getFullYear() 
              && lDate.getMonth()==todayDate.getMonth()
              && lDate.getDate()==todayDate.getDate()) {           // 是今天的日期
            _in_td_2.addClassName("cell_today");
          } else if (lDate.getDay()==0 || lDate.getDay()==6) {    // 周末
            _in_td_2.addClassName("cell_weekend");
          } else {                                                // 平日
            _in_td_2.addClassName("cell_weekday");
          }
          _in_td_2.addClassName("this_month");
          _in_td_2._ret = lDate.getFullYear() + pointer.dateSeparator + 
                          pointer.leftPad(""+(lDate.getMonth()+1)) + pointer.dateSeparator +  
                          pointer.leftPad(""+(lDate.getDate()));
          Event.observe(_in_td_2, 'click',  function(e){ pointer.decided(this._ret); });
        }
      }
    }
    // footer
    
    var _footer_tr = new Element("tr", {"class": "footer"}); _tbody_0.appendChild(_footer_tr); Event.observe(_footer_tr, 'mousedown', function(e) { e.stopPropagation(); e.preventDefault(); return false; } );
    var _footer_td = new Element("td"); _footer_tr.appendChild(_footer_td);

    var previous_y_link = new Element("a", {"href": "javascript:void(0)"}).update((year-1) + "年"); _footer_td.appendChild(previous_y_link);
    this.home_handler = function(e){ pointer.show(new Date(year-1, month-1, 1)); };
    Event.observe(previous_y_link, 'click', this.home_handler );
    _footer_td.appendChild(document.createTextNode(' '));
    var next_y_link = new Element("a", {"href": "javascript:void(0)"}).update((year+1) + "年"); _footer_td.appendChild(next_y_link);
    this.end_handler = function(e){ pointer.show(new Date(year+1, month-1, 1)); };
    Event.observe(next_y_link, 'click', this.end_handler );
    _footer_td.appendChild(document.createTextNode(' '));

    var close_link = new Element("a", {"href": "javascript:void(0)"}).update("关闭"); _footer_td.appendChild(close_link);
    Event.observe(close_link, 'click',  function(e){ pointer.close() } );

    this.div.appendChild(_table_0);
    if (this.iframe!=null){
      this.iframe.style.width = this.div.offsetWidth + 'px';
      this.iframe.style.height = this.div.offsetHeight + 'px';
    }
    
    
    
    
  },
  decided: function(dateStr) {
    this.input.value = dateStr; 
    if (this.decided_handler) {    // 选中之后回调
      this.decided_handler(dateStr);
    }
    this.close();
  }, 
  close: function(){
    if (this.div) {
      this.div.remove();
      this.div = null;
      if (this.pageup_handler) { this.pageup_handler = null }
      if (this.pagedown_handler) { this.pagedown_handler = null }
      Event.stopObserving(document, 'mousedown', this.doc_md_handler);    /* 图层关闭后移除监视 */
      Event.stopObserving(window,   'blur',      this.win_blur_handler);  /* 图层关闭后移除监视 */
      if (this.iframe) { this.iframe.remove(); this.iframe = null }
    }
  }


});