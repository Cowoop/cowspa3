(function(d){if(!Modernizr.genericDOM){var f=document,k,i,o=/<([\w:]+)/,m={option:1,optgroup:1,legend:1,thead:1,tr:1,td:1,col:1,area:1};d.webshims.fixHTML5=function(d){if("string"!=typeof d||m[(o.exec(d)||["",""])[1].toLowerCase()])return d;if(!i){k=f.body;if(!k)return d;i=f.createElement("div");i.style.display="none"}var p=i.cloneNode(!1);k.appendChild(p);p.innerHTML=d;k.removeChild(p);return p.childNodes}}})(jQuery);
jQuery.webshims.register("dom-extend",function(d,f,k,i,o){var m=f.modules,n=/\s*,\s*/,p={},r={},l={},g={},t={},j=d.fn.val,w=function(a,b,c,e,h){return h?j.call(d(a)):j.call(d(a),c)};d.fn.val=function(a){var b=this[0];arguments.length&&null==a&&(a="");if(!arguments.length)return!b||1!==b.nodeType?j.call(this):d.prop(b,"value",a,"val",!0);if(d.isArray(a))return j.apply(this,arguments);var c=d.isFunction(a);return this.each(function(e){b=this;1===b.nodeType&&(c?(e=a.call(b,e,d.prop(b,"value",o,"val",
!0)),null==e&&(e=""),d.prop(b,"value",e,"val")):d.prop(b,"value",a,"val"))})};var u="_webshimsLib"+Math.round(1E3*Math.random()),s=function(a,b,c){a=a.jquery?a[0]:a;if(!a)return c||{};var e=d.data(a,u);c!==o&&(e||(e=d.data(a,u,{})),b&&(e[b]=c));return b?e&&e[b]:e};[{name:"getNativeElement",prop:"nativeElement"},{name:"getShadowElement",prop:"shadowElement"},{name:"getShadowFocusElement",prop:"shadowFocusElement"}].forEach(function(a){d.fn[a.name]=function(){return this.map(function(){var b=s(this,
"shadowData");return b&&b[a.prop]||this})}});["removeAttr","prop","attr"].forEach(function(a){p[a]=d[a];d[a]=function(b,c,e,h,A){var g="val"==h,m=!g?p[a]:w;if(!b||!r[c]||1!==b.nodeType||!g&&h&&"attr"==a&&d.attrFn[c])return m(b,c,e,h,A);var y=(b.nodeName||"").toLowerCase(),f=l[y],n="attr"==a&&(!1===e||null===e)?"removeAttr":a,j,i,k;f||(f=l["*"]);f&&(f=f[c]);f&&(j=f[n]);if(j){if("value"==c)i=j.isVal,j.isVal=g;if("removeAttr"===n)return j.value.call(b);if(e===o)return j.get?j.get.call(b):j.value;j.set&&
("attr"==a&&!0===e&&(e=c),k=j.set.call(b,e));if("value"==c)j.isVal=i}else k=m(b,c,e,h,A);if((e!==o||"removeAttr"===n)&&t[y]&&t[y][c]){var q;q="removeAttr"==n?!1:"prop"==n?!!e:!0;t[y][c].forEach(function(c){if(!c.only||(c.only="prop"==a)||"attr"==c.only&&"prop"!=a)c.call(b,e,q,g?"val":n,a)})}return k};g[a]=function(b,c,e){l[b]||(l[b]={});l[b][c]||(l[b][c]={});var h=l[b][c][a],g=function(b,h,d){return h&&h[b]?h[b]:d&&d[b]?d[b]:"prop"==a&&"value"==c?function(b){return e.isVal?w(this,c,b,!1,0===arguments.length):
p[a](this,c,b)}:"prop"==a&&"value"==b&&e.value.apply?function(b){var e=p[a](this,c);e&&e.apply&&(e=e.apply(this,arguments));return e}:function(b){return p[a](this,c,b)}};l[b][c][a]=e;if(e.value===o){if(!e.set)e.set=e.writeable?g("set",e,h):f.cfg.useStrict&&"prop"==c?function(){throw c+" is readonly on "+b;}:d.noop;if(!e.get)e.get=g("get",e,h)}["value","get","set"].forEach(function(b){e[b]&&(e["_sup"+b]=g(b,h))})}});var z=!d.browser.msie||8<parseInt(d.browser.version,10),x=function(){var a=f.getPrototypeOf(i.createElement("foobar")),
b=Object.prototype.hasOwnProperty;return function(c,e,h){var d=i.createElement(c),g=f.getPrototypeOf(d);if(z&&g&&a!==g&&(!d[e]||!b.call(d,e))){var m=d[e];h._supvalue=function(){return m&&m.apply?m.apply(this,arguments):m};g[e]=h.value}else h._supvalue=function(){var b=s(this,"propValue");return b&&b[e]&&b[e].apply?b[e].apply(this,arguments):b&&b[e]},q.extendValue(c,e,h.value);h.value._supvalue=h._supvalue}}(),q=function(){var a={};f.addReady(function(b,c){var e={},g=function(a){e[a]||(e[a]=d(b.getElementsByTagName(a)),
c[0]&&d.nodeName(c[0],a)&&(e[a]=e[a].add(c)))};d.each(a,function(b,a){g(b);!a||!a.forEach?f.warn("Error: with "+b+"-property. methods: "+a):a.forEach(function(a){e[b].each(a)})});e=null});var b,c=d([]),e=function(c,e){a[c]?a[c].push(e):a[c]=[e];d.isDOMReady&&(b||d(i.getElementsByTagName(c))).each(e)};return{createTmpCache:function(a){d.isDOMReady&&(b=b||d(i.getElementsByTagName(a)));return b||c},flushTmpCache:function(){b=null},content:function(b,a){e(b,function(){var b=d.attr(this,a);null!=b&&d.attr(this,
a,b)})},createElement:function(b,a){e(b,a)},extendValue:function(b,a,c){e(b,function(){d(this).each(function(){s(this,"propValue",{})[a]=this[a];this[a]=c})})}}}(),v=function(a,b){if(a.defaultValue===o)a.defaultValue="";if(!a.removeAttr)a.removeAttr={value:function(){a[b||"prop"].set.call(this,a.defaultValue);a.removeAttr._supvalue.call(this)}}};d.extend(f,{getID:function(){var a=(new Date).getTime();return function(b){var b=d(b),c=b.attr("id");c||(a++,c="ID-"+a,b.attr("id",c));return c}}(),extendUNDEFProp:function(a,
b){d.each(b,function(b,e){b in a||(a[b]=e)})},createPropDefault:v,data:s,moveToFirstEvent:function(){var a=d._data?"_data":"data";return function(b,c,e){if((b=(d[a](b,"events")||{})[c])&&1<b.length)c=b.pop(),e||(e="bind"),"bind"==e&&b.delegateCount?b.splice(b.delegateCount,0,c):b.unshift(c)}}(),addShadowDom:function(a,b,c){c=c||{};a.jquery&&(a=a[0]);b.jquery&&(b=b[0]);if(!c.shadowFocusElement)c.shadowFocusElement=b;var e=d.data(a,u)||d.data(a,u,{}),h=d.data(b,u)||d.data(b,u,{});e.hasShadow=b;h.nativeElement=
a;h.shadowData=e.shadowData={nativeElement:a,shadowElement:b,shadowFocusElement:c.shadowFocusElement};c.shadowChilds&&c.shadowChilds.each(function(){s(this,"shadowData",h.shadowData)});if(c.data)e.shadowData.data=c.data,h.shadowData.data=c.data;c=null},propTypes:{standard:function(a){v(a);if(!a.prop)a.prop={set:function(b){a.attr.set.call(this,""+b)},get:function(){return a.attr.get.call(this)||a.defaultValue}}},"boolean":function(a){v(a);if(!a.prop)a.prop={set:function(b){b?a.attr.set.call(this,
""):a.removeAttr.value.call(this)},get:function(){return null!=a.attr.get.call(this)}}}},reflectProperties:function(a,b){"string"==typeof b&&(b=b.split(n));b.forEach(function(b){f.defineNodeNamesProperty(a,b,{prop:{set:function(a){d.attr(this,b,a)},get:function(){return d.attr(this,b)||""}}})})},defineNodeNameProperty:function(a,b,c){r[b]=!0;if(c.reflect)f.propTypes[c.propType||"standard"](c);["prop","attr","removeAttr"].forEach(function(e){var h=c[e];h&&(h="prop"===e?d.extend({writeable:!0},h):d.extend({},
h,{writeable:!0}),g[e](a,b,h),"*"!=a&&f.cfg.extendNative&&"prop"==e&&h.value&&d.isFunction(h.value)&&x(a,b,h),c[e]=h)});c.initAttr&&q.content(a,b);return c},defineNodeNameProperties:function(a,b,c,e){for(var d in b)!e&&b[d].initAttr&&q.createTmpCache(a),c&&(b[d][c]?f.log("override: "+a+"["+d+"] for "+c):(b[d][c]={},["value","set","get"].forEach(function(a){a in b[d]&&(b[d][c][a]=b[d][a],delete b[d][a])}))),b[d]=f.defineNodeNameProperty(a,d,b[d]);e||q.flushTmpCache();return b},createElement:function(a,
b,c){var e;d.isFunction(b)&&(b={after:b});q.createTmpCache(a);b.before&&q.createElement(a,b.before);c&&(e=f.defineNodeNameProperties(a,c,!1,!0));b.after&&q.createElement(a,b.after);q.flushTmpCache();return e},onNodeNamesPropertyModify:function(a,b,c,e){"string"==typeof a&&(a=a.split(n));d.isFunction(c)&&(c={set:c});a.forEach(function(a){t[a]||(t[a]={});"string"==typeof b&&(b=b.split(n));c.initAttr&&q.createTmpCache(a);b.forEach(function(b){t[a][b]||(t[a][b]=[],r[b]=!0);if(c.set){if(e)c.set.only=e;
t[a][b].push(c.set)}c.initAttr&&q.content(a,b)});q.flushTmpCache()})},defineNodeNamesBooleanProperty:function(a,b,c){c||(c={});if(d.isFunction(c))c.set=c;f.defineNodeNamesProperty(a,b,{attr:{set:function(a){this.setAttribute(b,a);c.set&&c.set.call(this,!0)},get:function(){return null==this.getAttribute(b)?o:b}},removeAttr:{value:function(){this.removeAttribute(b);c.set&&c.set.call(this,!1)}},reflect:!0,propType:"boolean",initAttr:c.initAttr||!1})},contentAttr:function(a,b,c){if(a.nodeName){if(c===
o)return c=(a.attributes[b]||{}).value,null==c?o:c;"boolean"==typeof c?c?a.setAttribute(b,b):a.removeAttribute(b):a.setAttribute(b,c)}},activeLang:function(){var a=[],b={},c,e,g=/:\/\/|^\.*\//,n=function(a,b,c){return b&&c&&-1!==d.inArray(b,c.availabeLangs||[])?(a.loading=!0,c=c.langSrc,g.test(c)||(c=f.cfg.basePath+c),f.loader.loadScript(c+b+".js",function(){a.langObj[b]?(a.loading=!1,j(a,!0)):d(function(){a.langObj[b]&&j(a,!0);a.loading=!1})}),!0):!1},l=function(a){b[a]&&b[a].forEach(function(a){a.callback()})},
j=function(a,b){if(a.activeLang!=c&&a.activeLang!==e){var d=m[a.module].options;if(a.langObj[c]||e&&a.langObj[e])a.activeLang=c,a.callback(a.langObj[c]||a.langObj[e],c),l(a.module);else if(!b&&!n(a,c,d)&&!n(a,e,d)&&a.langObj[""]&&""!==a.activeLang)a.activeLang="",a.callback(a.langObj[""],c),l(a.module)}};return function(g){if("string"==typeof g&&g!==c)c=g,e=c.split("-")[0],c==e&&(e=!1),d.each(a,function(a,b){j(b)});else if("object"==typeof g)if(g.register)b[g.register]||(b[g.register]=[]),b[g.register].push(g),
g.callback();else{if(!g.activeLang)g.activeLang="";a.push(g);j(g)}return c}}()});d.each({defineNodeNamesProperty:"defineNodeNameProperty",defineNodeNamesProperties:"defineNodeNameProperties",createElements:"createElement"},function(a,b){f[a]=function(a,e,d,g){"string"==typeof a&&(a=a.split(n));var m={};a.forEach(function(a){m[a]=f[b](a,e,d,g)});return m}});f.isReady("webshimLocalization",!0)});
(function(d,f){var k=d.webshims.browserVersion;if(!(d.browser.mozilla&&5<k)&&(!d.browser.msie||12>k&&7<k)){var i={article:"article",aside:"complementary",section:"region",nav:"navigation",address:"contentinfo"},o=function(d,n){d.getAttribute("role")||d.setAttribute("role",n)};d.webshims.addReady(function(m,n){d.each(i,function(g,f){for(var l=d(g,m).add(n.filter(g)),i=0,k=l.length;i<k;i++)o(l[i],f)});if(m===f){var p=f.getElementsByTagName("header")[0],k=f.getElementsByTagName("footer"),l=k.length;
p&&!d(p).closest("section, article")[0]&&o(p,"banner");l&&(p=k[l-1],d(p).closest("section, article")[0]||o(p,"contentinfo"))}})}})(jQuery,document);
(function(d,f,k){var i=f.audio&&f.video,o=!1;if(i)d=document.createElement("video"),f.videoBuffered="buffered"in d,o="loop"in d,k.capturingEvents("play,playing,waiting,paused,ended,durationchange,loadedmetadata,canplay,volumechange".split(",")),f.videoBuffered||(k.addPolyfill("mediaelement-native-fix",{f:"mediaelement",test:f.videoBuffered,d:["dom-support"]}),k.reTest("mediaelement-native-fix"));jQuery.webshims.register("mediaelement-core",function(d,f,k,r,l){var g=f.mediaelement,t=f.cfg.mediaelement,
j=function(a,b){var a=d(a),c={src:a.attr("src")||"",elem:a,srcProp:a.prop("src")};if(!c.src)return c;var e=a.attr("type");if(e)c.type=e,c.container=d.trim(e.split(";")[0]);else if(b||(b=a[0].nodeName.toLowerCase(),"source"==b&&(b=(a.closest("video, audio")[0]||{nodeName:"video"}).nodeName.toLowerCase())),e=g.getTypeForSrc(c.src,b))c.type=e,c.container=e,f.warn("you should always provide a proper mime-type using the source element. "+c.src+" detected as: "+e),d.nodeName(a[0],"source")&&a.attr("type",
e);if(e=a.attr("media"))c.media=e;return c},w=swfobject.hasFlashPlayerVersion("9.0.115"),u=function(){f.ready("mediaelement-swf",function(){if(!g.createSWF)f.modules["mediaelement-swf"].test=d.noop,f.reTest(["mediaelement-swf"],i)})};g.mimeTypes={audio:{"audio/ogg":["ogg","oga","ogm"],"audio/mpeg":["mp2","mp3","mpga","mpega"],"audio/mp4":"mp4,mpg4,m4r,m4a,m4p,m4b,aac".split(","),"audio/wav":["wav"],"audio/3gpp":["3gp","3gpp"],"audio/webm":["webm"],"audio/fla":["flv","f4a","fla"],"application/x-mpegURL":["m3u8",
"m3u"]},video:{"video/ogg":["ogg","ogv","ogm"],"video/mpeg":["mpg","mpeg","mpe"],"video/mp4":["mp4","mpg4","m4v"],"video/quicktime":["mov","qt"],"video/x-msvideo":["avi"],"video/x-ms-asf":["asf","asx"],"video/flv":["flv","f4v"],"video/3gpp":["3gp","3gpp"],"video/webm":["webm"],"application/x-mpegURL":["m3u8","m3u"],"video/MP2T":["ts"]}};g.mimeTypes.source=d.extend({},g.mimeTypes.audio,g.mimeTypes.video);g.getTypeForSrc=function(a,b){if(-1!=a.indexOf("youtube.com/watch?")||-1!=a.indexOf("youtube.com/v/"))return"video/youtube";
var a=a.split("?")[0].split("."),a=a[a.length-1],c;d.each(g.mimeTypes[b],function(b,d){if(-1!==d.indexOf(a))return c=b,!1});return c};g.srces=function(a,b){a=d(a);if(b)a.removeAttr("src").removeAttr("type").find("source").remove(),d.isArray(b)||(b=[b]),b.forEach(function(b){var c=r.createElement("source");"string"==typeof b&&(b={src:b});c.setAttribute("src",b.src);b.type&&c.setAttribute("type",b.type);b.media&&c.setAttribute("media",b.media);a.append(c)});else{var b=[],c=a[0].nodeName.toLowerCase(),
e=j(a,c);e.src?b.push(e):d("source",a).each(function(){e=j(this,c);e.src&&b.push(e)});return b}};d.fn.loadMediaSrc=function(a,b){return this.each(function(){b!==l&&(d(this).removeAttr("poster"),b&&d.attr(this,"poster",b));g.srces(this,a);d(this).mediaLoad()})};g.swfMimeTypes="video/3gpp,video/x-msvideo,video/quicktime,video/x-m4v,video/mp4,video/m4p,video/x-flv,video/flv,audio/mpeg,audio/aac,audio/mp4,audio/x-m4a,audio/m4a,audio/mp3,audio/x-fla,audio/fla,youtube/flv,jwplayer/jwplayer,video/youtube".split(",");
g.canSwfPlaySrces=function(a,b){var c="";w&&(a=d(a),b=b||g.srces(a),d.each(b,function(a,b){if(b.container&&b.src&&-1!=g.swfMimeTypes.indexOf(b.container))return c=b,!1}));return c};var s={};g.canNativePlaySrces=function(a,b){var c="";if(i){var a=d(a),e=(a[0].nodeName||"").toLowerCase();if(!s[e])return c;b=b||g.srces(a);d.each(b,function(b,d){if(d.type&&s[e].prop._supvalue.call(a[0],d.type))return c=d,!1})}return c};g.setError=function(a,b){b||(b="can't play sources");d(a).pause().data("mediaerror",
b);f.warn("mediaelementError: "+b);setTimeout(function(){d(a).data("mediaerror")&&d(a).trigger("mediaerror")},1)};var z=function(){var a;return function(b,c,d){f.ready("mediaelement-swf",function(){g.createSWF?g.createSWF(b,c,d):a||(a=!0,u(),z(b,c,d))})}}(),x=function(a,b,c,d,f){c||!1!==c&&b&&"flash"==b.isActive?(c=g.canSwfPlaySrces(a,d))?z(a,c,b):f?g.setError(a,!1):x(a,b,!1,d,!0):(c=g.canNativePlaySrces(a,d))?b&&"flash"==b.isActive&&g.setActive(a,"html5",b):f?(g.setError(a,!1),b&&"flash"==b.isActive&&
g.setActive(a,"html5",b)):x(a,b,!0,d,!0)},q=/^(?:embed|object)$/i,v=function(a,b){var c=f.data(a,"mediaelementBase")||f.data(a,"mediaelementBase",{}),e=g.srces(a),h=a.parentNode;clearTimeout(c.loadTimer);d.data(a,"mediaerror",!1);if(e.length&&h&&!q.test(h.nodeName||""))b=b||f.data(a,"mediaelement"),x(a,b,t.preferFlash||l,e)};d(r).bind("ended",function(a){var b=f.data(a.target,"mediaelement");(!o||b&&"html5"!=b.isActive||d.prop(a.target,"loop"))&&setTimeout(function(){!d.prop(a.target,"paused")&&d.prop(a.target,
"loop")&&d(a.target).prop("currentTime",0).play()},1)});o||f.defineNodeNamesBooleanProperty(["audio","video"],"loop");["audio","video"].forEach(function(a){var b=f.defineNodeNameProperty(a,"load",{prop:{value:function(){var a=f.data(this,"mediaelement");v(this,a);i&&(!a||"html5"==a.isActive)&&b.prop._supvalue&&b.prop._supvalue.apply(this,arguments)}}});s[a]=f.defineNodeNameProperty(a,"canPlayType",{prop:{value:function(b){var e="";i&&s[a].prop._supvalue&&(e=s[a].prop._supvalue.call(this,b),"no"==
e&&(e=""));!e&&w&&(b=d.trim((b||"").split(";")[0]),-1!=g.swfMimeTypes.indexOf(b)&&(e="maybe"));return e}}})});f.onNodeNamesPropertyModify(["audio","video"],["src","poster"],{set:function(){var a=this,b=f.data(a,"mediaelementBase")||f.data(a,"mediaelementBase",{});clearTimeout(b.loadTimer);b.loadTimer=setTimeout(function(){v(a);a=null},9)}});i&&f.isReady("mediaelement-core",!0);f.addReady(function(a,b){d("video, audio",a).add(b.filter("video, audio")).each(function(){d.browser.msie&&8<f.browserVersion&&
d.prop(this,"paused")&&!d.prop(this,"readyState")&&d(this).is('audio[preload="none"][controls]:not([autoplay])')?d(this).prop("preload","metadata").mediaLoad():v(this);if(i){var a,b,g=this,l=function(){var a=d.prop(g,"buffered");if(a){for(var b="",c=0,e=a.length;c<e;c++)b+=a.end(c);return b}},j=function(){var a=l();a!=b&&(b=a,d(g).triggerHandler("progress"))};d(this).bind("play loadstart progress",function(d){"progress"==d.type&&(b=l());clearTimeout(a);a=setTimeout(j,999)}).bind("emptied stalled mediaerror abort suspend",
function(d){"emptied"==d.type&&(b=!1);clearTimeout(a)})}})});i&&w&&f.ready("WINDOWLOAD mediaelement",u)})})(jQuery,Modernizr,jQuery.webshims);
jQuery.webshims.register("details",function(d,f,k,i,o,m){var n=function(f){var g=d(f).parent("details");if(g[0]&&g.children(":first").get(0)===f)return g},p=function(f,g){var f=d(f),g=d(g),i=d.data(g[0],"summaryElement");d.data(f[0],"detailsElement",g);if(!i||f[0]!==i[0])i&&(i.hasClass("fallback-summary")?i.remove():i.unbind(".summaryPolyfill").removeData("detailsElement").removeAttr("role").removeAttr("tabindex").removeAttr("aria-expanded").removeClass("summary-button").find("span.details-open-indicator").remove()),d.data(g[0],
"summaryElement",f),g.prop("open",g.prop("open"))};f.createElement("summary",function(){var f=n(this);if(f&&!d.data(this,"detailsElement")){var g;p(this,f);d(this).bind("focus.summaryPolyfill",function(){d(this).addClass("summary-has-focus")}).bind("blur.summaryPolyfill",function(){d(this).removeClass("summary-has-focus")}).bind("mouseenter.summaryPolyfill",function(){d(this).addClass("summary-has-hover")}).bind("mouseleave.summaryPolyfill",function(){d(this).removeClass("summary-has-hover")}).bind("click.summaryPolyfill",
function(d){var f=n(this);f&&(clearTimeout(g),g=setTimeout(function(){d.isDefaultPrevented()||f.prop("open",!f.prop("open"))},0))}).bind("keydown.summaryPolyfill",function(f){if((13==f.keyCode||32==f.keyCode)&&!f.isDefaultPrevented())f.preventDefault(),d(this).trigger("click")}).attr({tabindex:"0",role:"button"}).prepend('<span class="details-open-indicator" />')}});var r;f.defineNodeNamesBooleanProperty("details","open",function(f){var g=d(d.data(this,"summaryElement"));if(g){var i=f?"removeClass":
"addClass",j=d(this);if(!r&&m.animate){j.stop().css({width:"",height:""});var k={width:j.width(),height:j.height()}}g.attr("aria-expanded",""+f);j[i]("closed-details-summary").children().not(g[0])[i]("closed-details-child");!r&&m.animate&&(f={width:j.width(),height:j.height()},j.css(k).animate(f,{complete:function(){d(this).css({width:"",height:""})}}))}});f.createElement("details",function(){r=!0;var f=d.data(this,"summaryElement");f||(f=d("> summary:first-child",this),f[0]?p(f,this):(d(this).prependPolyfill('<summary class="fallback-summary">'+
m.text+"</summary>"),d.data(this,"summaryElement")));d.prop(this,"open",d.prop(this,"open"));r=!1})});
