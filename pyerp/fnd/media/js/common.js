/**
 * 功能:共通JS(ver0.1).
 * 
 * 1, 动态加入style.
 * 
 * @author 2009.7 yu.peng
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


/**  
 * 格式化数字显示方式
 * 用法
 * formatNumber(12345.999,'#,##0.00');
 * formatNumber(12345.999,'#,##0.##');
 * formatNumber(123,'000000');
 * @param num
 * @param pattern default '#,##0.00'
 * 
 * debug("formatNumber('','')=" + formatNumber('',''));
 * debug("formatNumber(123456789012.129,null)=" + formatNumber(123456789012.129,null));   
 * debug("formatNumber(null,null)=" + formatNumber(null,null));   
 * debug("formatNumber(123456789012.129,'#,##0.00')=" + formatNumber(123456789012.129,'#,##0.00'));   
 * debug("formatNumber(123456789012.129,'#,##0.##')=" + formatNumber(123456789012.129,'#,##0.##'));   
 * debug("formatNumber(123456789012.129,'#0.00')=" + formatNumber(123456789012.129,'#,##0.00'));   
 * debug("formatNumber(123456789012.129,'#0.##')=" + formatNumber(123456789012.129,'#,##0.##'));   
 * debug("formatNumber(12.129,'0.00')=" + formatNumber(12.129,'0.00'));   
 * debug("formatNumber(12.129,'0.##')=" + formatNumber(12.129,'0.##'));   
 * debug("formatNumber(12,'00000')=" + formatNumber(12,'00000'));   
 * debug("formatNumber(12,'#.##')=" + formatNumber(12,'#.##'));   
 * debug("formatNumber(12,'#.00')=" + formatNumber(12,'#.00'));   
 * debug("formatNumber(0,'#.##')=" + formatNumber(0,'#.##'));
 * 
 * 
 */
function formatNumber(num, pattern){
  if (num==null) return "";
  pattern = pattern ? pattern : '#0.00';
  var strarr = num ? num.toString().split('.'):['0'];
  var fmtarr = pattern ? pattern.split('.'):[''];
  var retstr='';
  
  // 整数部分
  var str = strarr[0];
  var fmt = fmtarr[0];
  var i = str.length-1;
  var comma = false;
  for(var f=fmt.length-1;f>=0;f--){
    switch(fmt.substr(f,1)){
      case '#':
        if(i>=0 ) retstr = str.substr(i--,1) + retstr;
        break;
      case '0':
        if(i>=0) retstr = str.substr(i--,1) + retstr;
        else retstr = '0' + retstr;   
        break;
      case ',':
        comma = true;
        retstr=','+retstr;
        break;
    }
  }
  if(i>=0){
    if(comma){
      var l = str.length;
      for(;i>=0;i--){
        retstr = str.substr(i,1) + retstr;
        if(i>0 && ((l-i)%3)==0) retstr = ',' + retstr;
      }
    }
    else retstr = str.substr(0,i+1) + retstr;
  }
  
  retstr = retstr+'.';
  // 处理小数部分   
  str=strarr.length>1?strarr[1]:'';
  fmt=fmtarr.length>1?fmtarr[1]:'';
  i=0;
  for(var f=0;f<fmt.length;f++){
    switch(fmt.substr(f,1)){
      case '#':
        if(i<str.length) retstr+=str.substr(i++,1);
        break;
      case '0':
        if(i<str.length) retstr+= str.substr(i++,1);
        else retstr+='0';
        break;
    }
  }
  return retstr.replace(/^,+/,'').replace(/\.$/,'');
}










