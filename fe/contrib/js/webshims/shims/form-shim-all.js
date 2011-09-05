Modernizr.formvalidation||jQuery.webshims.register("form-extend",function(a,c,p,k){c.inputTypes=c.inputTypes||{};var o=c.cfg.forms,i,g=function(a){return typeof a=="number"||a&&a==a*1},m=c.inputTypes,j={radio:1,checkbox:1};c.addInputType=function(a,b){m[a]=b};var n={customError:!1,typeMismatch:!1,rangeUnderflow:!1,rangeOverflow:!1,stepMismatch:!1,tooLong:!1,patternMismatch:!1,valueMissing:!1,valid:!0},e={valueMissing:function(l,b,d){if(!l.attr("required"))return!1;var f=!1;if(!("type"in d))d.type=
(l[0].getAttribute("type")||l[0].type||"").toLowerCase();if(d.nodeName=="select"){if(b=!b)if(!(b=l[0].selectedIndex<0))l=l[0],b=l.type=="select-one"&&l.size<2?!!a("> option:first-child",l).prop("selected"):!1;l=b}else l=j[d.type]?d.type=="checkbox"?!l.is(":checked"):!a(l[0].form&&l[0].name?l[0].form[l[0].name]:[]).filter(":checked")[0]:!b;return l},tooLong:function(a,b,d){if(b===""||d.nodeName=="select")return!1;var a=a.attr("maxlength"),d=!1,f=b.length;f&&a>=0&&b.replace&&g(a)&&(d=f>a);return d},
typeMismatch:function(a,b,d){if(b===""||d.nodeName=="select")return!1;var f=!1;if(!("type"in d))d.type=(a[0].getAttribute("type")||a[0].type||"").toLowerCase();m[d.type]&&m[d.type].mismatch&&(f=m[d.type].mismatch(b,a));return f},patternMismatch:function(a,b,d){if(b===""||d.nodeName=="select")return!1;a=a.attr("pattern");if(!a)return!1;a=RegExp("^(?:"+a+")$");return!a?!1:!a.test(b)}};c.addValidityRule=function(a,b){e[a]=b};a.event.special.invalid={add:function(){a.event.special.invalid.setup.call(this.form||
this)},setup:function(){var b=this.form||this;if(!a.data(b,"invalidEventShim"))a(b).data("invalidEventShim",!0).bind("submit",a.event.special.invalid.handler),(b=a(b).data("events").submit)&&b.length>1&&b.unshift(b.pop())},teardown:a.noop,handler:function(b){if(!(b.type!="submit"||b.testedValidity||!b.originalEvent||!a.nodeName(b.target,"form")||a.prop(b.target,"noValidate"))){i=!0;b.testedValidity=!0;if(!a(b.target).checkValidity())return this===k&&c.warn("always embed HTML5 content using .prependWebshim, .appendWebshim, .htmlWebshim etc."),
b.stopImmediatePropagation(),i=!1;i=!1}}};a(k).bind("invalid",a.noop);a.event.special.submit=a.event.special.submit||{setup:function(){return!1}};var b=a.event.special.submit.setup;a.extend(a.event.special.submit,{setup:function(){a.nodeName(this,"form")?a(this).bind("invalid",a.noop):a("form",this).bind("invalid",a.noop);return b.apply(this,arguments)}});c.addInputType("email",{mismatch:function(){var a=o.emailReg||/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|(\x22((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?\x22))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)*(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i;
return function(b){return!a.test(b)}}()});c.addInputType("url",{mismatch:function(){var a=o.urlReg||/^([a-z]([a-z]|\d|\+|-|\.)*):(\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?((\[(|(v[\da-f]{1,}\.(([a-z]|\d|-|\.|_|~)|[!\$&'\(\)\*\+,;=]|:)+))\])|((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=])*)(:\d*)?)(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*|(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)|((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)|((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)){0})(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i;
return function(b){return!a.test(b)}}()});c.defineNodeNamesProperties(["button","fieldset","output"],{checkValidity:{value:function(){return!0}},willValidate:{value:!1},setCustomValidity:{value:a.noop},validity:{writeable:!1,get:function(){return a.extend({},n)}}},"prop");var h=function(b){var d,f=a.prop(b,"validity");if(f)a.data(b,"cachedValidity",f);else return!0;if(!f.valid){d=a.Event("invalid");var e=a(b).trigger(d);if(i&&!h.unhandledInvalids&&!d.isDefaultPrevented())c.validityAlert.showFor(e),
h.unhandledInvalids=!0}a.removeData(b,"cachedValidity",!1);return f.valid};c.defineNodeNameProperty("form","checkValidity",{prop:{value:function(){var b=!0,d=a("input,textarea,select",this).filter(function(){var a=c.data(this,"shadowData");return!a||!a.nativeElement||a.nativeElement===this});h.unhandledInvalids=!1;for(var f=0,e=d.length;f<e;f++)h(d[f])||(b=!1);return b}}});c.defineNodeNamesProperties(["input","textarea","select"],{checkValidity:{value:function(){h.unhandledInvalids=!1;return h(a(this).getNativeElement()[0])}},
setCustomValidity:{value:function(a){c.data(this,"customvalidationMessage",""+a)}},willValidate:{set:a.noop,get:function(){var b={button:1,reset:1,hidden:1,image:1};return function(){var d=a(this).getNativeElement()[0];return!(d.disabled||d.readOnly||b[d.type]||d.form&&a.prop(d.form,"noValidate"))}}()},validity:{set:a.noop,get:function(){var b=a(this).getNativeElement(),d=b[0],f=a.data(d,"cachedValidity");if(f)return f;f=a.extend({},n);if(!a.prop(d,"willValidate")||d.type=="submit")return f;var h=
b.val(),g={nodeName:d.nodeName.toLowerCase()};f.customError=!!c.data(d,"customvalidationMessage");if(f.customError)f.valid=!1;a.each(e,function(a,d){if(d(b,h,g))f[a]=!0,f.valid=!1});d.setAttribute("aria-invalid",f.valid?"false":"true");d=b=null;return f}}},"prop");c.defineNodeNamesBooleanProperty(["input","textarea","select"],"required",{set:function(a){this.setAttribute("aria-required",!!a+"")},initAttr:!0});c.reflectProperties(["input"],["pattern"]);c.defineNodeNameProperty("textarea","maxlength",
{attr:{set:function(a){this.setAttribute("maxlength",""+a)},get:function(){var a=this.getAttribute("maxlength");return a==null?void 0:a}},prop:{set:function(a){if(g(a)){if(a<0)throw"INDEX_SIZE_ERR";this.setAttribute("maxlength",parseInt(a,10))}else this.setAttribute("maxlength","0")},get:function(){var a=this.getAttribute("maxlength");return g(a)&&a>=0?parseInt(a,10):-1}}});c.defineNodeNameProperty("textarea","maxLength",{prop:{set:function(b){a.prop(this,"maxlength",b)},get:function(){return a.prop(this,
"maxlength")}}});var f={submit:1,button:1,image:1},d={};[{name:"enctype",limitedTo:{"application/x-www-form-urlencoded":1,"multipart/form-data":1,"text/plain":1},defaultProp:"application/x-www-form-urlencoded",proptype:"enum"},{name:"method",limitedTo:{get:1,post:1},defaultProp:"get",proptype:"enum"},{name:"action",proptype:"url"},{name:"target"},{name:"novalidate",propName:"noValidate",proptype:"boolean"}].forEach(function(b){var h="form"+(b.propName||b.name).replace(/^[a-z]/,function(a){return a.toUpperCase()}),
e="form"+b.name,c=b.name,g="click.webshimssubmittermutate"+c,n=function(){if("form"in this&&f[this.type]){var d=a.prop(this,"form");if(d){var g=a.attr(this,e);if(g!=null&&(!b.limitedTo||g.toLowerCase()===a.prop(this,h))){var n=a.attr(d,c);a.attr(d,c,g);setTimeout(function(){n!=null?a.attr(d,c,n):a(d).removeAttr(c)},9)}}}};switch(b.proptype){case "url":var j=k.createElement("form");d[h]={prop:{set:function(b){a.attr(this,e,b)},get:function(){var b=a.attr(this,e);if(b==null)return"";j.setAttribute("action",
b);return j.action}}};break;case "boolean":d[h]={prop:{set:function(b){b?a.attr(this,"formnovalidate","formnovalidate"):a(this).removeAttr("formnovalidate")},get:function(){return a.attr(this,"formnovalidate")!=null}}};break;case "enum":d[h]={prop:{set:function(b){a.attr(this,e,b)},get:function(){var d=a.attr(this,e);return!d||(d=d.toLowerCase())&&!b.limitedTo[d]?b.defaultProp:d}}};break;default:d[h]={prop:{set:function(b){a.attr(this,e,b)},get:function(){var b=a.attr(this,e);return b!=null?b:""}}}}d[e]||
(d[e]={});d[e].attr={set:function(b){d[e].attr._supset.call(this,b);a(this).unbind(g).bind(g,n)},get:function(){return d[e].attr._supget.call(this)}};d[e].initAttr=!0;d[e].removeAttr={value:function(){a(this).unbind(g);d[e].removeAttr._supvalue.call(this)}}});c.defineNodeNamesProperties(["input","button"],d);!a.support.getSetAttribute&&a("<form novalidate></form>").attr("novalidate")==null&&c.defineNodeNameProperty("form","novalidate",{attr:{set:function(a){this.setAttribute("novalidate",""+a)},get:function(){var a=
this.getAttribute("novalidate");return a==null?void 0:a}}});c.defineNodeNameProperty("form","noValidate",{prop:{set:function(b){b?a.attr(this,"novalidate","novalidate"):a(this).removeAttr("novalidate")},get:function(){return a.attr(this,"novalidate")!=null}}});c.addReady(function(b,d){a("form",b).add(d.filter("form")).bind("invalid",a.noop);setTimeout(function(){try{if(k.activeElement&&"form"in k.activeElement)return}catch(d){return}var f=!0;a("input, select, textarea",b).each(function(){if(!f)return!1;
if(this.getAttribute("autofocus")!=null){f=!1;var b=a(this).getShadowFocusElement();try{b[0].focus()}catch(d){}return!1}})},0)})});
jQuery.webshims.ready("dom-support form-core",function(a,c,p){Modernizr.textareaPlaceholder=!!("placeholder"in a("<textarea />")[0]);if(!Modernizr.input.placeholder||!Modernizr.textareaPlaceholder){var k=c.cfg.forms.placeholderType=="over",o=["textarea"];Modernizr.input.placeholder||o.push("input");var i=function(c,e,b){if(!k&&c.type!="password")b===!1&&(b=a.prop(c,"value")),c.value=b;e.box.removeClass("placeholder-visible")},g=function(c,e,b,h,f){if(!h&&(h=a.data(c,"placeHolder"),!h))return;if(f==
"focus"||!f&&c===document.activeElement)(c.type=="password"||k||a(c).hasClass("placeholder-visible"))&&i(c,h,"");else if(e===!1&&(e=a.prop(c,"value")),e)i(c,h,e);else if(b===!1&&(b=a.attr(c,"placeholder")||""),b&&!e){e=h;b===!1&&(b=a.attr(c,"placeholder")||"");if(!k&&c.type!="password")c.value=b;e.box.addClass("placeholder-visible")}else i(c,h,e)},m=function(c){var c=a(c),e=c.prop("id"),b=!(!c.attr("title")&&!c.attr("aria-labeledby"));!b&&e&&(b=!!a('label[for="'+e+'"]',c[0].form)[0]);return a(b?'<span class="placeholder-text"></span>':
'<label for="'+(e||a.webshims.getID(c))+'" class="placeholder-text"></label>')},j=function(){var c={text:1,search:1,url:1,email:1,password:1,tel:1};return{create:function(e){var b=a.data(e,"placeHolder");if(b)return b;b=a.data(e,"placeHolder",{text:m(e)});a(e).bind("focus.placeholder blur.placeholder",function(a){g(this,!1,!1,b,a.type)});e.form&&a(e.form).bind("reset.placeholder",function(a){setTimeout(function(){g(e,!1,!1,b,a.type)},0)});if(e.type=="password"||k){b.box=a(e).wrap('<span class="placeholder-box placeholder-box-'+
(e.nodeName||"").toLowerCase()+'" />').parent();b.text.insertAfter(e).bind("mousedown.placeholder",function(){g(this,!1,!1,b,"focus");try{setTimeout(function(){e.focus()},0)}catch(a){}return!1});a.each(["Left","Top"],function(d,f){var c=(parseInt(a.curCSS(e,"padding"+f),10)||0)+Math.max(parseInt(a.curCSS(e,"margin"+f),10)||0,0)+(parseInt(a.curCSS(e,"border"+f+"Width"),10)||0);b.text.css("padding"+f,c)});a.curCSS(e,"lineHeight");var c={width:a(e).width(),height:a(e).height()},f=a.curCSS(e,"float");
a.each(["lineHeight","fontSize","fontFamily","fontWeight"],function(d,f){var c=a.curCSS(e,f);b.text.css(f)!=c&&b.text.css(f,c)});c.width&&c.height&&b.text.css(c);f!=="none"&&b.box.addClass("placeholder-box-"+f)}else{c=function(d){a(e).hasClass("placeholder-visible")&&(i(e,b,""),d&&d.type=="submit"&&setTimeout(function(){d.isDefaultPrevented()&&g(e,!1,!1,b)},9))};if(a.nodeName(b.text[0],"label"))b.text.hide()[a.browser.msie?"insertBefore":"insertAfter"](e);a(p).bind("beforeunload",c);b.box=a(e);e.form&&
a(e.form).submit(c)}return b},update:function(e,b){if(c[a.prop(e,"type")]||a.nodeName(e,"textarea")){var h=j.create(e);h.text.text(b);g(e,!1,b,h)}}}}();a.webshims.publicMethods={pHolder:j};o.forEach(function(a){c.defineNodeNameProperty(a,"placeholder",{attr:{set:function(a){c.contentAttr(this,"placeholder",a);j.update(this,a)},get:function(){return c.contentAttr(this,"placeholder")}},reflect:!0,initAttr:!0})});o.forEach(function(j){var e={},b;["attr","prop"].forEach(function(h){e[h]={set:function(a){var d=
c.contentAttr(this,"placeholder"),e=b[h]._supset.call(this,a);d&&"value"in this&&g(this,a,d);return e},get:function(){return a(this).hasClass("placeholder-visible")?"":b[h]._supget.call(this)}}});b=c.defineNodeNameProperty(j,"value",e)})}});
jQuery.webshims.ready("dom-support",function(a,c,p,k,o){c.propTypes.element=function(i){c.createPropDefault(i,"attr");if(!i.prop)i.prop={get:function(){var c=i.attr.get.call(this);c&&(c=a("#"+c)[0])&&i.propNodeName&&!a.nodeName(c,i.propNodeName)&&(c=null);return c||null},writeable:!1}};(function(){if(!("value"in k.createElement("output"))){c.defineNodeNameProperty("output","value",{prop:{set:function(c){var m=a.data(this,"outputShim");m||(m=i(this));m(c)},get:function(){return c.contentAttr(this,
"value")||a(this).text()||""}}});c.onNodeNamesPropertyModify("input","value",function(c,i,j){j!="removeAttr"&&(i=a.data(this,"outputShim"))&&i(c)});var i=function(g){if(!g.getAttribute("aria-live")){var g=a(g),i=(g.text()||"").trim(),j=g.attr("id"),n=g.attr("for"),e=a('<input class="output-shim" type="hidden" name="'+(g.attr("name")||"")+'" value="'+i+'" style="display: none" />').insertAfter(g),b=e[0].form||k,h=function(a){e[0].value=a;a=e[0].value;g.text(a);c.contentAttr(g[0],"value",a)};g[0].defaultValue=
i;c.contentAttr(g[0],"value",i);g.attr({"aria-live":"polite"});j&&(e.attr("id",j),g.attr("aria-labeldby",c.getID(a('label[for="'+j+'"]',b))));n&&(j=c.getID(g),n.split(" ").forEach(function(a){(a=k.getElementById(a))&&a.setAttribute("aria-controls",j)}));g.data("outputShim",h);e.data("outputShim",h);return h}};c.addReady(function(c,k){a("output",c).add(k.filter("output")).each(function(){i(this)})})}})();(function(){if(!Modernizr.datalist){var i=0,g={submit:1,button:1,reset:1,hidden:1,range:1,date:1},
m=a.browser.msie&&parseInt(a.browser.version,10)<7,j={},n=function(a){if(!a)return[];if(j[a])return j[a];var e;c.ready("json-storage",function(){try{e=JSON.parse(localStorage.getItem("storedDatalistOptions"+a))}catch(c){}j[a]=e||[]});return e||[]},e={_create:function(b){if(!g[(b.input.getAttribute("type")||"").toLowerCase()||b.input.type]){var c=b.datalist,f=a.data(b.input,"datalistWidget");if(c&&f&&f.datalist!==c)f.datalist=c,f.id=b.id,f._resetListCached();else if(c){if(!(f&&f.datalist===c)){i++;
var d=this;this.timedHide=function(){clearTimeout(d.hideTimer);d.hideTimer=setTimeout(a.proxy(d,"hideList"),9)};this.datalist=c;this.id=b.id;this.lazyIDindex=i;this.hasViewableData=!0;this._autocomplete=a.attr(b.input,"autocomplete");a.data(b.input,"datalistWidget",this);this.shadowList=a('<div class="datalist-polyfill" />').appendTo("body");this.index=-1;this.input=b.input;this.arrayOptions=[];this.shadowList.delegate("li","mouseover.datalistWidget mousedown.datalistWidget click.datalistWidget",
function(b){var c=a("li:not(.hidden-item)",d.shadowList),f=b.type=="mousedown"||b.type=="click";d.markItem(c.index(b.target),f,c);b.type=="click"&&d.hideList();return b.type!="mousedown"}).bind("focusout",this.timedHide);b.input.setAttribute("autocomplete","off");a(b.input).attr({"aria-haspopup":"true"}).bind("input.datalistWidget",a.proxy(this,"showHideOptions")).bind("keydown.datalistWidget",function(b){var c=b.keyCode;if(c==40&&!d.showList())return d.markItem(d.index+1,!0),!1;if(d.isListVisible){if(c==
38)return d.markItem(d.index-1,!0),!1;if(!b.shiftKey&&(c==33||c==36))return d.markItem(0,!0),!1;if(!b.shiftKey&&(c==34||c==35))return b=a("li:not(.hidden-item)",d.shadowList),d.markItem(b.length-1,!0,b),!1;if(c==13||c==27)return c==13&&(b=a("li.active-item:not(.hidden-item)",d.shadowList),b[0]&&(a.prop(d.input,"value",b.attr("data-value")),a(d.input).triggerHandler("updateInput"))),d.hideList(),!1}}).bind("focus.datalistWidget",function(){a(this).hasClass("list-focus")&&d.showList()}).bind("blur.datalistWidget",
this.timedHide);a(this.datalist).unbind("updateDatalist.datalistWidget").bind("updateDatalist.datalistWidget",a.proxy(this,"_resetListCached"));this._resetListCached();b.input.form&&b.input.id&&a(b.input.form).bind("submit.datalistWidget"+b.input.id,function(){var c=a.prop(b.input,"value");d.storedOptions=n(b.input.name||b.input.id);if(c&&a.inArray(c,d.storedOptions)==-1){d.storedOptions.push(c);var c=b.input.name||b.input.id,f=d.storedOptions;if(c){f=f||[];try{localStorage.setItem("storedDatalistOptions"+
c,JSON.stringify(f))}catch(e){}}}});a(p).bind("unload",function(){d.destroy()})}}else f&&f.destroy()}},destroy:function(){var b=a.attr(this.input,"autocomplete");a(this.input).unbind(".datalistWidget").removeData("datalistWidget");this.shadowList.remove();a(k).unbind(".datalist"+this.id);this.input.form&&this.input.id&&a(this.input.form).unbind("submit.datalistWidget"+this.input.id);this.input.removeAttribute("aria-haspopup");b===o?this.input.removeAttribute("autocomplete"):a(this.input).attr("autocomplete",
b)},_resetListCached:function(){var a=this;this.needsUpdate=!0;this.lastUpdatedValue=!1;this.lastUnfoundValue="";if(!this.updateTimer)this.updateTimer=setTimeout(function(){a.updateListOptions()},this.isListVisible||p.QUnit?0:40*this.lazyIDindex)},updateListOptions:function(){this.needsUpdate=!1;clearTimeout(this.updateTimer);this.updateTimer=!1;this.shadowList.css({fontSize:a.curCSS(this.input,"fontSize"),fontFamily:a.curCSS(this.input,"fontFamily")});var b='<ul role="list" class="'+(this.datalist.className||
"")+" "+this.datalist.id+'-shadowdom">',c=[],f=[];a("option",this.datalist).each(function(b){if(!this.disabled){var e={value:a(this).val()||"",text:a.trim(a.attr(this,"label")||this.textContent||this.innerText||a.text([this])||""),className:this.className||"",style:a.attr(this,"style")||""};if(!e.text)e.text=e.value;c[b]=e.value;f[b]=e}});this.storedOptions=n(this.input.name||this.input.id);this.storedOptions.forEach(function(b){a.inArray(b,c)==-1&&f.push({value:b,text:b,className:"",style:""})});
f.forEach(function(a){var c=a.value.indexOf('"')!=-1?"'"+a.value+"'":'"'+a.value+'"';b+="<li data-value="+c+' class="'+a.className+'" style="'+a.style+'" tabindex="-1" role="listitem">'+a.text+"</li>"});b+="</ul>";this.arrayOptions=f;this.shadowList.html(b);a.fn.bgIframe&&m&&this.shadowList.bgIframe();this.isListVisible&&this.showHideOptions()},showHideOptions:function(){var b=a.prop(this.input,"value").toLowerCase();if(!(b===this.lastUpdatedValue||this.lastUnfoundValue&&b.indexOf(this.lastUnfoundValue)===
0)){this.lastUpdatedValue=b;var c=!1,f=a("li",this.shadowList);b?this.arrayOptions.forEach(function(d,e){if(!("lowerText"in d))d.lowerText=d.text.toLowerCase(),d.lowerValue=d.value.toLowerCase();d.lowerText.indexOf(b)!==-1||d.lowerValue.indexOf(b)!==-1?(a(f[e]).removeClass("hidden-item"),c=!0):a(f[e]).addClass("hidden-item")}):(f.removeClass("hidden-item"),c=!0);(this.hasViewableData=c)?this.showList():(this.lastUnfoundValue=b,this.hideList())}},showList:function(){if(this.isListVisible)return!1;
this.needsUpdate&&this.updateListOptions();this.showHideOptions();if(!this.hasViewableData)return!1;var b=this,c=a(this.input).offset();c.top+=a(this.input).outerHeight();c.width=a(this.input).outerWidth()-(parseInt(this.shadowList.css("borderLeftWidth"),10)||0)-(parseInt(this.shadowList.css("borderRightWidth"),10)||0);m&&(this.shadowList.css("height","auto"),this.shadowList.height()>250&&this.shadowList.css("height",220));this.shadowList.css(c).addClass("datalist-visible");this.isListVisible=!0;
a(k).bind("mousedown.datalist"+this.id+" focusin.datalist"+this.id,function(c){c.target===b.input||b.shadowList[0]===c.target||a.contains(b.shadowList[0],c.target)?(clearTimeout(b.hideTimer),setTimeout(function(){clearTimeout(b.hideTimer)},0)):b.timedHide()});return!0},hideList:function(){if(!this.isListVisible)return!1;this.shadowList.removeClass("datalist-visible list-item-active").scrollTop(0).find("li.active-item").removeClass("active-item");this.index=-1;this.isListVisible=!1;a(this.input).removeAttr("aria-activedescendant");
a(k).unbind(".datalist"+this.id);return!0},scrollIntoView:function(b){var c=a("> ul",this.shadowList),f=b.position();f.top-=(parseInt(c.css("paddingTop"),10)||0)+(parseInt(c.css("marginTop"),10)||0)+(parseInt(c.css("borderTopWidth"),10)||0);f.top<0?this.shadowList.scrollTop(this.shadowList.scrollTop()+f.top-2):(f.top+=b.outerHeight(),b=this.shadowList.height(),f.top>b&&this.shadowList.scrollTop(this.shadowList.scrollTop()+(f.top-b)+2))},markItem:function(b,c,f){f=f||a("li:not(.hidden-item)",this.shadowList);
if(f.length)b<0?b=f.length-1:b>=f.length&&(b=0),f.removeClass("active-item"),this.shadowList.addClass("list-item-active"),f=f.filter(":eq("+b+")").addClass("active-item"),c&&(a.prop(this.input,"value",f.attr("data-value")),a.attr(this.input,"aria-activedescendant",a.webshims.getID(f)),a(this.input).triggerHandler("updateInput"),this.scrollIntoView(f)),this.index=b}};(function(){c.defineNodeNameProperties("input",{list:{attr:{get:function(){var a=c.contentAttr(this,"list");return a==null?o:a},set:function(b){c.contentAttr(this,
"list",b);c.objectCreate(e,o,{input:this,id:b,datalist:a.prop(this,"list")})}},initAttr:!0,reflect:!0,propType:"element",propNodeName:"datalist"},selectedOption:{prop:{writeable:!1,get:function(){var b=a.prop(this,"list"),c=null,f;if(!b)return c;f=a.attr(this,"value");if(!f)return c;b=a.prop(b,"options");if(!b.length)return c;a.each(b,function(b,e){if(f==a.prop(e,"value"))return c=e,!1});return c}}},autocomplete:{attr:{get:function(){var b=a.data(this,"datalistWidget");return b?b._autocomplete:"autocomplete"in
this?this.autocomplete:this.getAttribute("autocomplete")},set:function(b){var c=a.data(this,"datalistWidget");c?(c._autocomplete=b,b=="off"&&c.hideList()):"autocomplete"in this?this.autocomplete=b:this.setAttribute("autocomplete",b)}}}});c.defineNodeNameProperty("datalist","options",{prop:{writeable:!1,get:function(){var b=a("select",this);return b[0]?b[0].options:[]}}});c.addReady(function(b,c){c.filter("select, option").each(function(){var b=this.parentNode,c=a.nodeName(b,"datalist");if(b&&!c)b=
b.parentNode,c=a.nodeName(b,"datalist");b&&c&&a(b).triggerHandler("updateDatalist")})})})()}})();(function(){var i={updateInput:1,input:1},g={radio:1,checkbox:1,submit:1,button:1,image:1,reset:1,file:1,color:1},m=function(a){var g,e=a.prop("value"),b=function(b){if(a){var d=a.prop("value");d!==e&&(e=d,(!b||!i[b.type])&&c.triggerInlineForm&&c.triggerInlineForm(a[0],"input"))}},h,f=function(){clearTimeout(h);h=setTimeout(b,9)},d=function(){a.unbind("focusout",d).unbind("keyup keypress keydown paste cut",
f).unbind("input change updateInput",b);clearInterval(g);setTimeout(function(){b();a=null},1)};clearInterval(g);g=setInterval(b,99);f();a.bind("keyup keypress keydown paste cut",f).bind("focusout",d).bind("input updateInput change",b)};a(k).bind("focusin",function(c){c.target&&c.target.type&&!c.target.readOnly&&!c.target.disabled&&(c.target.nodeName||"").toLowerCase()=="input"&&!g[c.target.type]&&m(a(c.target))})})();c.modules["form-output-datalist"]&&c.isReady("form-output-datalist",!0)});
