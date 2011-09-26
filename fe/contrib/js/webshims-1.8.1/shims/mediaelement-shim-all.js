jQuery.webshims.ready('dom-support', function($, webshims, window, document, undefined){
	
	var anchor = document.createElement('a');
	['poster', 'src'].forEach(function(prop){
		webshims.defineNodeNamesProperty(prop == 'src' ? ['audio', 'video', 'source'] : ['video'], prop, {
			prop: {
				get: function(){
					var href = this.getAttribute(prop);
					if(href == null){return '';}
					anchor.setAttribute('href', href+'' );
					return !$.support.hrefNormalized ? anchor.getAttribute('href', 4) : anchor.href;
				},
				set: function(src){
					$.attr(this, prop, src);
				}
			}
		});
	});
	
	
	['autoplay', 'controls'].forEach(function(name){
		webshims.defineNodeNamesBooleanProperty(['audio', 'video'], name);
	});
		
	webshims.defineNodeNamesProperties(['audio', 'video'], {
		HAVE_CURRENT_DATA: {
			value: 2
		},
		HAVE_ENOUGH_DATA: {
			value: 4
		},
		HAVE_FUTURE_DATA: {
			value: 3
		},
		HAVE_METADATA: {
			value: 1
		},
		HAVE_NOTHING: {
			value: 0
		},
		NETWORK_EMPTY: {
			value: 0
		},
		NETWORK_IDLE: {
			value: 1
		},
		NETWORK_LOADING: {
			value: 2
		},
		NETWORK_NO_SOURCE: {
			value: 3
		}
				
	}, 'prop');
	

});/*
 * todos: 
 * - flashblocker detect
 * - decouple muted/volume
 * - improve buffered-property with youtube/rtmp
 * - get buffer-full event
 * - set preload to none, if flash is active
 * - use jwplayer5 api instead of old flash4 api (this can be scheduled)
 */

jQuery.webshims.register('mediaelement-swf', function($, webshims, window, document, undefined, options){
	"use strict";
	var mediaelement = webshims.mediaelement;
	var swfobject = window.swfobject;
	var hasNative = Modernizr.audio && Modernizr.video;
	var hasFlash = swfobject.hasFlashPlayerVersion('9.0.115');
	var loadedSwf = 0;
	var getProps = {
		paused: true,
		ended: false,
		currentSrc: '',
		duration: window.NaN,
		
		readyState: 0,
		networkState: 0,
		videoHeight: 0,
		videoWidth: 0,
		error: null,
		buffered: {
			start: function(index){
				if(index){
					webshims.error('buffered index size error');
					return;
				}
				return 0;
			},
			end: function(index){
				if(index){
					webshims.error('buffered index size error');
					return;
				}
				return 0;
			},
			length: 0
		}
	};
	var getPropKeys = Object.keys(getProps);
	
	var getSetProps = {
		currentTime: 0,
		volume: 1,
		muted: false
	};
	var getSetPropKeys = Object.keys(getSetProps);
	
	var playerStateObj = $.extend({
		isActive: 'html5',
		activating: 'html5',	
		wasSwfReady: false,
		_bufferedEnd: 0,
		_bufferedStart: 0,
		_metadata: false,
		_callMeta: false,
		currentTime: 0,
		_ppFlag: undefined
	}, getProps, getSetProps);
	
	var idRep = /^jwplayer-/;
	var getSwfDataFromID = function(id){
		
		var elem = document.getElementById(id.replace(idRep, ''));
		if(!elem){return;}
		var data = webshims.data(elem, 'mediaelement');
		return data.isActive == 'flash' ? data : null;
	};
	
	
	var getSwfDataFromElem = function(elem){
		try {
			(elem.nodeName);
		} catch(er){
			return null;
		}
		var data = webshims.data(elem, 'mediaelement');
		return (data && data.isActive== 'flash') ? data : null;
	};
	
	var trigger = function(elem, evt){
		evt = $.Event(evt);
		evt.preventDefault();
		$.event.trigger(evt, undefined, elem);
	};
	var stopMutedAnnounce;
	var playerSwfPath = options.playerPath || webshims.cfg.basePath + "jwplayer/" + (options.playerName || "player.swf");
	var jwplugin = options.pluginPath || webshims.cfg.basePath +'swf/jwwebshims.swf';
	
	webshims.extendUNDEFProp(options.jwParams, {
		allowscriptaccess: 'always',
		allowfullscreen: 'true',
		wmode: 'transparent'
	});
	webshims.extendUNDEFProp(options.jwVars, {
		screencolor: 'ffffffff'
	});
	webshims.extendUNDEFProp(options.jwAttrs, {
		bgcolor: '#000000'
	});
	
	mediaelement.jwEvents = {
		View: {
			
			PLAY: function(obj){
				var data = getSwfDataFromID(obj.id);
				if(!data || data.stopPlayPause){return;}
				data._ppFlag = true;
				if(data.paused == obj.state){
					data.paused = !obj.state;
					if(data.ended){
						data.ended = false;
					}
					trigger(data._elem, obj.state ? 'play' : 'pause');
				}
			}
		},
		Model: {
			
			BUFFER: function(obj){
				var data = getSwfDataFromID(obj.id);
				if(!data){return;}
				if(data._bufferedEnd == obj.percentage){return;}
				data.networkState = (obj.percentage == 100) ? 1 : 2;
				if(!data.duration){
					try {
						data.duration = data.jwapi.getPlaylist()[0].duration;
						if(data.duration <= 0){
							data.duration = window.NaN;
						}
					} catch(er){}
					if(data.duration){
						trigger(data._elem, 'durationchange');
						if(data._elemNodeName == 'audio' || data._callMeta){
							this.META($.extend({duration: data.duration}, obj), data);
						}
					}
				}
				if(data.ended){
					data.ended = false;
				}
				if(!data.duration){
					return;
				}
				
				if(obj.percentage > 1 && data.readyState < 3){
					data.readyState = 3;
					trigger(data._elem, 'canplay');
				}
				if(data._bufferedEnd && (data._bufferedEnd > obj.percentage)){
					data._bufferedStart = data.currentTime || 0;
				}
				
				data._bufferedEnd = obj.percentage;
				data.buffered.length = 1;
				if(obj.percentage == 100){
					data.networkState = 1;
					data.readyState = 4;
				}
				$.event.trigger('progress', undefined, data._elem, true);
			},
			META: function(obj, data){
				
				
				
				data = data && data.networkState ? data : getSwfDataFromID(obj.id);
				if( !('duration' in obj) ){
					data._callMeta = true;
					return;
				}
				
				
				if(!data || data._metadata ){return;}
				data._metadata = true;
								
				var oldDur = data.duration;
				data.duration = obj.duration;
				data.videoHeight = obj.height || 0;
				data.videoWidth = obj.width || 0;
				if(!data.networkState){
					data.networkState = 2;
				}
				if(data.readyState < 1){
					data.readyState = 1;
				}
				if(oldDur !== data.duration){
					trigger(data._elem, 'durationchange');
				}
				
				trigger(data._elem, 'loadedmetadata');
			},
			TIME: function(obj){
				var data = getSwfDataFromID(obj.id);
				if(!data || data.currentTime === obj.position){return;}
				data.currentTime = obj.position;
				if(data.readyState < 2){
					data.readyState = 2;
				}
				if(data.ended){
					data.ended = false;
				}
				trigger(data._elem, 'timeupdate');
				
			},
			STATE: function(obj){
				var data = getSwfDataFromID(obj.id);
				if(!data){return;}
				switch(obj.newstate) {
					case 'BUFFERING':
						if(data.readyState > 1){
							data.readyState = 1;
						}
						if(data.ended){
							data.ended = false;
						}
						trigger(data._elem, 'waiting');
						break;
					case 'PLAYING':
						data.paused = false;
						data._ppFlag = true;
						if(data.readyState < 3){
							data.readyState = 3;
							trigger(data._elem, 'canplay');
						}
						if(data.ended){
							data.ended = false;
						}
						trigger(data._elem, 'playing');
						break;
					case 'PAUSED':
						if(!data.paused && !data.stopPlayPause){
							data.paused = true;
							data._ppFlag = true;
							trigger(data._elem, 'pause');
						}
						break;
					case 'COMPLETED':
						if(data.readyState < 4){
							data.readyState = 4;
						}
						data.ended = true;
						trigger(data._elem, 'ended');
						break;
				}
			}
		}
		,Controller: {
			
			ERROR: function(obj){
				var data = getSwfDataFromID(obj.id);
				if(!data){return;}
				mediaelement.setError(data._elem, obj.message);
			},
			SEEK: function(obj){
				var data = getSwfDataFromID(obj.id);
				if(!data){return;}
				if(data.ended){
					data.ended = false;
				}
				if(data.paused){
					try {
						data.jwapi.sendEvent('play', 'false');
					} catch(er){}
				}
				if(data.currentTime != obj.position){
					data.currentTime = obj.position;
					trigger(data._elem, 'timeupdate');
				}
				
				
			},
			VOLUME: function(obj){
				var data = getSwfDataFromID(obj.id);
				if(!data){return;}
				var newVolume = obj.percentage / 100;
				if(data.volume == newVolume){return;}
				data.volume = newVolume;
				trigger(data._elem, 'volumechange');
			},
			MUTE: function(obj){
				if(stopMutedAnnounce && obj.state){return;}
				var data = getSwfDataFromID(obj.id);
				if(!data){return;}
				if(data.muted == obj.state){return;}
				data.muted = obj.state;
				trigger(data._elem, 'volumechange');
			}
		}
	};
	
	var initEvents = function(data){
		$.each(mediaelement.jwEvents, function(mvcName, evts){
			$.each(evts, function(evtName){
				data.jwapi['add'+ mvcName +'Listener'](evtName, 'jQuery.webshims.mediaelement.jwEvents.'+ mvcName +'.'+ evtName);
			});
		});
	};
	
	var workActionQueue = function(data){
		var actionLen = data.actionQueue.length;
		var i = 0;
		var operation;
		if(actionLen && data.isActive == 'flash'){
			while(data.actionQueue.length && actionLen > i){
				i++;
				operation = data.actionQueue.shift();
				data.jwapi[operation.fn].apply(data.jwapi, operation.args);
			}
		}
		if(data.actionQueue.length){
			data.actionQueue = [];
		}
	};
	var startAutoPlay = function(data){
		if(!data){return;}
		if( (data._ppFlag === undefined && ($.prop(data._elem, 'autoplay')) || !data.paused)){
			setTimeout(function(){
				if(data.isActive == 'flash' && (data._ppFlag === undefined || !data.paused)){
					try {
						$(data._elem).play();
					} catch(er){}
				}
			}, 1);
		}
	};
	
	var startIntrinsicDimension = function(data){
		if(!data || data._elemNodeName != 'video'){return;}
		var img;
		var widthAuto;
		var heightAuto;
		var lastIntrinsicSize = {};
		var shadowElem;
		var errorTimer;
		var blockResize;
		var lastSize;
		var setSize = function(width, height){
			if(!height || !width || height < 1 || width < 1 || data.isActive != 'flash'){return;}
			if(img){
				img.remove();
				img = false;
			}
			lastIntrinsicSize.width = width;
			lastIntrinsicSize.height = height;
			clearTimeout(errorTimer);
			widthAuto = data._elem.style.width == 'auto';
			heightAuto = data._elem.style.height == 'auto';
			
			if(!widthAuto && !heightAuto){return;}
			var curSize;
			shadowElem = shadowElem || $(data._elem).getShadowElement();
			var cur;
			if(widthAuto && !heightAuto){
				cur = shadowElem.height();
				width *=  cur / height;
				height = cur;
			} else if(!widthAuto && heightAuto){
				cur = shadowElem.width();
				height *=  cur / width;
				width = cur;
			}
			blockResize = true;
			setTimeout(function(){
				blockResize = false;
			}, 9);
			
			shadowElem.css({width: width, height: height});
		};
		var setPosterSrc = function(){
			if(data.isActive != 'flash' || ($.prop(data._elem, 'readyState') && $.prop(this, 'videoWidth'))){return;}
			var posterSrc = $.prop(data._elem, 'poster');
			if(!posterSrc){return;}
			widthAuto = data._elem.style.width == 'auto';
			heightAuto = data._elem.style.height == 'auto';
			if(!widthAuto && !heightAuto){return;}
			if(img){
				img.remove();
				img = false;
			}
			img = $('<img style="position: absolute; height: auto; width: auto; top: 0px; left: 0px; visibility: hidden;" />');
			img
				.bind('load error alreadycomplete', function(e){
					clearTimeout(errorTimer);
					
					var elem = this;
					var width = elem.naturalWidth || elem.width || elem.offsetWidth;
					var height = elem.naturalHeight || elem.height || elem.offsetHeight;
					
					if(height && width){
						setSize(width, height);
						elem = null;
					} else {
						setTimeout(function(){
							width = elem.naturalWidth || elem.width || elem.offsetWidth;
							height = elem.naturalHeight || elem.height || elem.offsetHeight;
							setSize(width, height);
							if(img){
								img.remove();
								img = false;
							}
							elem = null;
						}, 9);
					}
					$(this).unbind();
				})
				.prop('src', posterSrc)
				.appendTo('body')
				.each(function(){
					if(this.complete || this.error){
						$(this).triggerHandler('alreadycomplete');
					} else {
						clearTimeout(errorTimer);
						errorTimer = setTimeout(function(){
							$(data._elem).triggerHandler('error');
						}, 9999);
					}
				})
			;
		};
		$(data._elem)
			.bind('loadedmetadata', function(){
				setSize($.prop(this, 'videoWidth'), $.prop(this, 'videoHeight'));
			})
			.bind('emptied', setPosterSrc)
			.bind('swfstageresize', function(){
				if(blockResize){return;}
				setSize(lastIntrinsicSize.width, lastIntrinsicSize.height);
			})
			.bind('emptied', function(){
				lastIntrinsicSize = {};
			})
			.triggerHandler('swfstageresize')
		;
		
		setPosterSrc();
		if($.prop(data._elem, 'readyState')){
			setSize($.prop(data._elem, 'videoWidth'), $.prop(data._elem, 'videoHeight'));
		}
	};
	
	mediaelement.playerResize = function(id){
		if(!id){return;}
		var elem = document.getElementById(id.replace(idRep, ''));
		
		if(elem){
			$(elem).triggerHandler('swfstageresize');
		}
		elem = null;
	};
	
	
	$(document).bind('emptied', function(e){
		var data = getSwfDataFromElem(e.target);
		startAutoPlay(data);
	});
	
	var localConnectionTimer;
	mediaelement.jwPlayerReady = function(jwData){
		var data = getSwfDataFromID(jwData.id);
		if(!data || !data.jwapi){return;}
		clearTimeout(localConnectionTimer);
		data.jwData = jwData;
		if(!data.wasSwfReady){
			var version = parseFloat( jwData.version, 10);
			if(version < 5.6 || version >= 6){
				webshims.warn('mediaelement-swf is only testet with jwplayer 5.6+');
			}
			$.prop(data._elem, 'volume', data.volume);
			$.prop(data._elem, 'muted', data.muted);
			initEvents(data);
			
		} else {
			$(data._elem).mediaLoad();
		}
		data.wasSwfReady = true;
		workActionQueue(data);
		startAutoPlay(data);
	};
	
	var addMediaToStopEvents = $.noop;
	if(hasNative){
		var stopEvents = {
			play: 1,
			playing: 1
		};
		var hideEvtArray = ['play', 'pause', 'playing', 'canplay', 'progress', 'waiting', 'ended', 'loadedmetadata', 'durationchange', 'emptied'];
		var hidevents = hideEvtArray.map(function(evt){
			return evt +'.webshimspolyfill';
		}).join(' ');
		
		var hidePlayerEvents = function(event){
			var data = webshims.data(event.target, 'mediaelement');
			if(!data){return;}
			var isNativeHTML5 = ( event.originalEvent && event.originalEvent.type === event.type );
			if( isNativeHTML5 == (data.activating == 'flash') ){
				event.stopImmediatePropagation();
				if(stopEvents[event.type] && data.isActive != data.activating){
					$(event.target).pause();
				}
			}
		};
		
		addMediaToStopEvents = function(elem){
			$(elem)
				.unbind(hidevents)
				.bind(hidevents, hidePlayerEvents)
			;
			hideEvtArray.forEach(function(evt){
				webshims.moveToFirstEvent(elem, evt);
			});
		};
		addMediaToStopEvents(document);
	}
	
	
	mediaelement.setActive = function(elem, type, data){
		if(!data){
			data = webshims.data(elem, 'mediaelement');
		}
		if(!data || data.isActive == type){return;}
		if(type != 'html5' && type != 'flash'){
			webshims.warn('wrong type for mediaelement activating: '+ type);
		}
		var shadowData = webshims.data(elem, 'shadowData');
		data.activating = type;
		$(elem).pause();
		data.isActive = type;
		if(type == 'flash'){
			shadowData.shadowElement = shadowData.shadowFocusElement = data.shadowElem[0];
			$(elem).hide().getShadowElement().show();
		} else {
			$(elem).show().getShadowElement().hide();
			shadowData.shadowElement = shadowData.shadowFocusElement = false;
		}
		
	};
	
	
	
	var resetSwfProps = (function(){
		var resetProtoProps = ['_bufferedEnd', '_bufferedStart', '_metadata', '_ppFlag', 'currentSrc', 'currentTime', 'duration', 'ended', 'networkState', 'paused', 'videoHeight', 'videoWidth', '_callMeta'];
		var len = resetProtoProps.length;
		return function(data){
			
			if(!data){return;}
			var lenI = len;
			var networkState = data.networkState;
			while(--lenI){
				delete data[resetProtoProps[lenI]];
			}
			data.actionQueue = [];
			data.buffered.length = 0;
			if(networkState){
				trigger(data._elem, 'emptied');
			}
		};
	})();
	
	mediaelement.createSWF = function( elem, canPlaySrc, data ){
		if(!hasFlash){
			setTimeout(function(){
				$(elem).mediaLoad(); //<- this should produce a mediaerror
			}, 1);
			return;
		}
		
		if(loadedSwf < 1){
			loadedSwf = 1;
		} else {
			loadedSwf++;
		}
		var vars = $.extend({}, options.jwVars, {
				image: $.prop(elem, 'poster') || '',
				file: canPlaySrc.srcProp
		});
		var elemVars = $(elem).data('jwvars') || {};
		
		if(data && data.swfCreated){
			mediaelement.setActive(elem, 'flash', data);
			resetSwfProps(data);
			data.currentSrc = canPlaySrc.srcProp;
			$.extend(vars, elemVars);
			options.changeJW(vars, elem, canPlaySrc, data, 'load');
			queueSwfMethod(elem, 'sendEvent', ['LOAD', vars]);
			
			return;
		}
		
		
		var hasControls = $.prop(elem, 'controls');
		var elemId = 'jwplayer-'+ webshims.getID(elem);
		
		
		var params = $.extend(
			{},
			options.jwParams,
			$(elem).data('jwparams')
		);
		var elemNodeName = elem.nodeName.toLowerCase();
		var attrs = $.extend(
			{},
			options.jwAttrs,
			{
				name: elemId,
				id: elemId
			},
			$(elem).data('jwattrs')
		);
		var box = $('<div class="polyfill-'+ (elemNodeName) +' polyfill-mediaelement" id="wrapper-'+ elemId +'"><div id="'+ elemId +'"></div>')
			.css({
				position: 'relative',
				overflow: 'hidden'
			})
		;
		if(elemNodeName == 'audio' && !hasControls){
			box.css({width: 0, height: 0});
		} else {
			box.css({
				width: elem.style.width || $(elem).width(),
				height: elem.style.height || $(elem).height()
			});
		}
		box.insertBefore(elem);
		data = webshims.data(elem, 'mediaelement', webshims.objectCreate(playerStateObj, {
			actionQueue: {
				value: []
			},
			shadowElem: {
				value: box
			},
			_elemNodeName: {
				value: elemNodeName
			},
			_elem: {
				value: elem
			},
			currentSrc: {
				value: canPlaySrc.srcProp
			},
			swfCreated: {
				value: true
			},
			buffered: {
				value: {
				start: function(index){
					if(index >= data.buffered.length){
						webshims.error('buffered index size error');
						return;
					}
					return 0;
				},
				end: function(index){
					if(index >= data.buffered.length){
						webshims.error('buffered index size error');
						return;
					}
					return ( (data.duration - data._bufferedStart) * data._bufferedEnd / 100) + data._bufferedStart;
				},
				length: 0
			}
			}
		}));
		
		if(hasNative){
			$.extend(data, {volume: $.prop(elem, 'volume'), muted: $.prop(elem, 'muted')});
		}
		
		$.extend(vars, 
			{
				id: elemId,
				controlbar: hasControls ? options.jwVars.controlbar || (elemNodeName == 'video' ? 'over' : 'bottom') : 'none',
				icons: ''+ (hasControls && elemNodeName == 'video')
			},
			elemVars,
			{playerready: 'jQuery.webshims.mediaelement.jwPlayerReady'}
		);
		if(vars.plugins){
			vars.plugins += ','+jwplugin;
		} else {
			vars.plugins = jwplugin;
		}
		
		
		webshims.addShadowDom(elem, box);
		addMediaToStopEvents(elem);
		mediaelement.setActive(elem, 'flash', data);
		options.changeJW(vars, elem, canPlaySrc, data, 'embed');
		startIntrinsicDimension(data);
		swfobject.embedSWF(playerSwfPath, elemId, "100%", "100%", "9.0.0", false, vars, params, attrs, function(swfData){
			if(swfData.success){
				data.jwapi = swfData.ref;
				if(!hasControls){
					$(swfData.ref).attr('tabindex', '-1').css('outline', 'none');
				}
				if(!localConnectionTimer){
					clearTimeout(localConnectionTimer);
					localConnectionTimer = setTimeout(function(){
						var elem = $(swfData.ref).css({'minHeight': '2px', 'minWidth': '2px', display: 'block'});
						if(elem[0].offsetWidth > 1 && elem[0].offsetHeight > 1 && location.protocol.indexOf('file:') === 0){
							webshims.warn("Add your local development-directory to the local-trusted security sandbox:  http://www.macromedia.com/support/documentation/en/flashplayer/help/settings_manager04.html");
						} else if(elem[0].offsetWidth < 2 || elem[0].offsetHeight < 2) {
							webshims.info("JS-SWF connection can't be established on hidden or unconnected flash objects");
						}
						elem = null;
					}, 8000);
				}
			}
		});
	};
	
	var SENDEVENT = 'sendEvent';
	var queueSwfMethod = function(elem, fn, args, data){
		data = data || getSwfDataFromElem(elem);
		if(data){
			if(data.jwapi && data.jwapi[fn]){
				data.jwapi[fn].apply(data.jwapi, args || []);
			} else {
				//todo add to queue
				data.actionQueue.push({fn: fn, args: args});
				if(data.actionQueue.length > 10){
					setTimeout(function(){
						if(data.actionQueue.length > 5){
							data.actionQueue.shift();
						}
					}, 99);
				}
			}
			return data;
		}
		return false;
	};
	
	['audio', 'video'].forEach(function(nodeName){
		var descs = {};
		var mediaSup;
		var createGetProp = function(key){
			if(nodeName == 'audio' && (key == 'videoHeight' || key == 'videoWidth')){return;}
			
			descs[key] = {
				get: function(){
					var data = getSwfDataFromElem(this);
					if(data){
						return data[key];
					} else if(hasNative && mediaSup[key].prop._supget) {
						return mediaSup[key].prop._supget.apply(this);
					} else {
						return playerStateObj[key];
					}
				},
				writeable: false
			};
		};
		var createGetSetProp = function(key, setFn){
			createGetProp(key);
			delete descs[key].writeable;
			descs[key].set = setFn;
		};
		
		createGetSetProp('volume', function(v){
			var data = getSwfDataFromElem(this);
			if(data){
				v *= 100;
				if(!isNaN(v)){
					if(v < 0 || v > 100){
						webshims.error('volume greater or less than allowed '+ (v / 100));
					}
					if(data.muted){
						stopMutedAnnounce = true;
					}
					queueSwfMethod(this, SENDEVENT, ['VOLUME', v], data);
					if(stopMutedAnnounce){
						try {
							data.jwapi.sendEvent('mute', 'true');
						} catch(er){}
						stopMutedAnnounce = false;
					}
					setTimeout(function(){
						v /= 100;
						if(data.volume == v || data.isActive != 'flash'){return;}
						data.volume = v;
						trigger(data._elem, 'volumechange');
						data = null;
					}, 1);	
				} 
			} else if(mediaSup.volume.prop._supset) {
				return mediaSup.volume.prop._supset.apply(this, arguments);
			}
		});
		
		createGetSetProp('muted', function(m){
			var data = getSwfDataFromElem(this);
			if(data){
				m = !!m;
				queueSwfMethod(this, SENDEVENT, ['mute', ''+m], data);
				setTimeout(function(){
					if(data.muted == m || data.isActive != 'flash'){return;}
					data.muted = m;
					trigger(data._elem, 'volumechange');
					data = null;
				}, 1); 
			} else if(mediaSup.muted.prop._supset) {
				return mediaSup.muted.prop._supset.apply(this, arguments);
			}
		});
		
		
		createGetSetProp('currentTime', function(t){
			var data = getSwfDataFromElem(this);
			if(data){
				t *= 1;
				if (!isNaN(t)) {
					if(data.paused){
						clearTimeout(data.stopPlayPause);
						data.stopPlayPause = setTimeout(function(){
							data.paused = true;
							data.stopPlayPause = false;
						}, 50);
					}
					queueSwfMethod(this, SENDEVENT, ['SEEK', '' + t], data);
					
					if(data.paused){
						if(data.readyState > 0){
							data.currentTime = t;
							trigger(data._elem, 'timeupdate');
						}
						try {
							data.jwapi.sendEvent('play', 'false');
						} catch(er){}
						
					}
				}
				 
			} else if(mediaSup.currentTime.prop._supset) {
				return mediaSup.currentTime.prop._supset.apply(this, arguments);
			}
		});
		
		['play', 'pause'].forEach(function(fn){
			descs[fn] = {
				value: function(){
					var data = getSwfDataFromElem(this);
					if(data){
						if(data.stopPlayPause){
							clearTimeout(data.stopPlayPause);
						}
						queueSwfMethod(this, SENDEVENT, ['play', fn == 'play'], data);
						setTimeout(function(){
							if(data.isActive == 'flash'){
								data._ppFlag = true;
								if(data.paused != (fn != 'play')){
									data.paused = fn != 'play';
									trigger(data._elem, fn);
								}
							}
						}, 1);
					} else if(mediaSup[fn].prop._supvalue) {
						return mediaSup[fn].prop._supvalue.apply(this, arguments);
					}
				}
			};
		});
		
		getPropKeys.forEach(createGetProp);
		
		webshims.onNodeNamesPropertyModify(nodeName, 'controls', function(val, boolProp){
			var data = queueSwfMethod(this, boolProp ? 'showControls' : 'hideControls', [nodeName]);
			$(this)[boolProp ? 'addClass' : 'removeClass']('webshims-controls');
			
			if(data){
				$(data.jwapi).attr('tabindex', boolProp ? '0' : '-1');
			}
		});
		
		mediaSup = webshims.defineNodeNameProperties(nodeName, descs, 'prop');
	});
	
	if(hasFlash){
		var oldClean = $.cleanData;
		var gcBrowser = $.browser.msie && webshims.browserVersion < 9;
		var flashNames = {
			object: 1,
			OBJECT: 1
		};
		$.cleanData = function(elems){
			var i, len, prop;
			if(elems && (len = elems.length) && loadedSwf){
				
				for(i = 0; i < len; i++){
					if(flashNames[elems[i].nodeName]){
						if(SENDEVENT in elems[i]){
							loadedSwf--;
							try {
								elems[i][SENDEVENT]('play', false);
							} catch(er){}
						}
						if(gcBrowser){
							try {
								for (prop in elems[i]) {
									if (typeof elems[i][prop] == "function") {
										elems[i][prop] = null;
									}
								}
							} catch(er){}
						}
					}
				}
				
			}
			return oldClean.apply(this, arguments);
		};
	}
	
});(function($, Modernizr, webshims){
	"use strict";
	var hasNative = Modernizr.audio && Modernizr.video;
	var supportsLoop = false;
	
	if(hasNative){
		var videoElem = document.createElement('video');
		Modernizr.videoBuffered = ('buffered' in videoElem);
		supportsLoop = ('loop' in videoElem);
		
		webshims.capturingEvents(['play', 'playing', 'waiting', 'paused', 'ended', 'durationchange', 'loadedmetadata', 'canplay', 'volumechange']);
		
		if(!Modernizr.videoBuffered){
			webshims.addPolyfill('mediaelement-native-fix', {
				feature: 'mediaelement',
				test: Modernizr.videoBuffered,
				dependencies: ['dom-support']
			});
			
			if(webshims.cfg.waitReady){
				$.readyWait++;
			}
			webshims.loader.loadScript('mediaelement-native-fix', function(){
				if(webshims.cfg.waitReady){
					$.ready(true);
				}
			});
		}
	}

$.webshims.ready('dom-support swfobject', function($, webshims, window, document, undefined){
	var mediaelement = webshims.mediaelement;
	var options = webshims.cfg.mediaelement;
	var getSrcObj = function(elem, nodeName){
		elem = $(elem);
		var src = {src: elem.attr('src') || '', elem: elem, srcProp: elem.prop('src')};
		if(!src.src){return src;}
		var tmp = elem.attr('type');
		if(tmp){
			src.type = tmp;
			src.container = $.trim(tmp.split(';')[0]);
		} else {
			if(!nodeName){
				nodeName = elem[0].nodeName.toLowerCase();
				if(nodeName == 'source'){
					nodeName = (elem.closest('video, audio')[0] || {nodeName: 'video'}).nodeName.toLowerCase();
				}
			}
			tmp = mediaelement.getTypeForSrc(src.src, nodeName );
			
			if(tmp){
				src.type = tmp;
				src.container = tmp;
				webshims.warn('you should always provide a proper mime-type using the source element. '+ src.src +' detected as: '+ tmp);
				if($.nodeName(elem[0], 'source')){
					elem.attr('type', tmp);
				}
			}
		}
		tmp = elem.attr('media');
		if(tmp){
			src.media = tmp;
		}
		return src;
	};
	
	
	var hasSwf = swfobject.hasFlashPlayerVersion('9.0.115');
	var loadSwf = function(){
		webshims.ready('mediaelement-swf', function(){
			if(!mediaelement.createSWF){
				//reset readyness (hacky way)
				webshims.modules["mediaelement-swf"].test = false;
				delete $.event.special["mediaelement-swfReady"];
				//load mediaelement-swf
				webshims.loader.loadList(["mediaelement-swf"]);
			}
		});
	};
	if(hasSwf){
		webshims.ready('WINDOWLOAD', loadSwf);
	}
	
	mediaelement.mimeTypes = {
		audio: {
				//ogm shouldn´t be used!
				'audio/ogg': ['ogg','oga', 'ogm'],
				'audio/mpeg': ['mp2','mp3','mpga','mpega'],
				'audio/mp4': ['mp4','mpg4', 'm4r'],
				'audio/wav': ['wav'],
				'audio/x-m4a': ['m4a'],
				'audio/x-m4p': ['m4p'],
				'audio/3gpp': ['3gp','3gpp'],
				'audio/webm': ['webm']
			},
			video: {
				//ogm shouldn´t be used!
				'video/ogg': ['ogg','ogv', 'ogm'],
				'video/mpeg': ['mpg','mpeg','mpe'],
				'video/mp4': ['mp4','mpg4', 'm4v'],
				'video/quicktime': ['mov','qt'],
				'video/x-msvideo': ['avi'],
				'video/x-ms-asf': ['asf', 'asx'],
				'video/flv': ['flv', 'f4v'],
				'video/3gpp': ['3gp','3gpp'],
				'video/webm': ['webm']
			}
		}
	;
	
	mediaelement.mimeTypes.source =  $.extend({}, mediaelement.mimeTypes.audio, mediaelement.mimeTypes.video);
	
	mediaelement.getTypeForSrc = function(src, nodeName){
		if(src.indexOf('youtube.com/watch?') != -1){
			return 'video/youtube';
		}
		src = src.split('?')[0].split('.');
		src = src[src.length - 1];
		var mt;
		
		$.each(mediaelement.mimeTypes[nodeName], function(mimeType, exts){
			if(exts.indexOf(src) !== -1){
				mt = mimeType;
				return false;
			}
		});
		return mt;
	};
	
	
	mediaelement.srces = function(mediaElem, srces){
		mediaElem = $(mediaElem);
		if(!srces){
			srces = [];
			var nodeName = mediaElem[0].nodeName.toLowerCase();
			var src = getSrcObj(mediaElem, nodeName);
			
			if(!src.src){
				
				$('source', mediaElem).each(function(){
					src = getSrcObj(this, nodeName);
					if(src.src){srces.push(src);}
				});
			} else {
				srces.push(src);
			}
			return srces;
		} else {
			mediaElem.removeAttr('src').removeAttr('type').find('source').remove();
			if(!$.isArray(srces)){
				srces = [srces]; 
			}
			srces.forEach(function(src){
				var source = document.createElement('source');
				if(typeof src == 'string'){
					src = {src: src};
				} 
				source.setAttribute('src', src.src);
				if(src.type){
					source.setAttribute('type', src.type);
				}
				if(src.media){
					source.setAttribute('media', src.media);
				}
				mediaElem.append(source);
			});
			
		}
	};
	
	
	$.fn.loadMediaSrc = function(srces, poster){
		return this.each(function(){
			if(poster !== undefined){
				$(this).removeAttr('poster');
				if(poster){
					$.attr(this, 'poster', poster);
				}
			}
			mediaelement.srces(this, srces);
			$(this).mediaLoad();
		});
	};
	
	mediaelement.swfMimeTypes = ['video/3gpp', 'video/x-msvideo', 'video/quicktime', 'video/x-m4v', 'video/mp4', 'video/m4p', 'video/x-flv', 'video/flv', 'audio/mpeg', 'audio/aac', 'audio/mp4', 'audio/x-m4a', 'audio/m4a', 'audio/mp3', 'audio/x-fla', 'audio/fla', 'youtube/flv', 'jwplayer/jwplayer', 'video/youtube'];
	mediaelement.canSwfPlaySrces = function(mediaElem, srces){
		var ret = '';
		if(hasSwf){
			mediaElem = $(mediaElem);
			srces = srces || mediaelement.srces(mediaElem);
			$.each(srces, function(i, src){
				if(src.container && src.src && mediaelement.swfMimeTypes.indexOf(src.container) != -1){
					ret = src;
					return false;
				}
			});
			
		}
		
		return ret;
	};
	
	var nativeCanPlayType = {};
	mediaelement.canNativePlaySrces = function(mediaElem, srces){
		var ret = '';
		if(hasNative){
			mediaElem = $(mediaElem);
			var nodeName = (mediaElem[0].nodeName || '').toLowerCase();
			if(!nativeCanPlayType[nodeName]){return ret;}
			srces = srces || mediaelement.srces(mediaElem);
			
			$.each(srces, function(i, src){
				if(src.type && nativeCanPlayType[nodeName].prop._supvalue.call(mediaElem[0], src.type) ){
					ret = src;
					return false;
				}
			});
		}
		return ret;
	};
	
	mediaelement.setError = function(elem, message){
		if(!message){
			message = "can't play sources";
		}
		
		$(elem).data('mediaerror', message);
		webshims.warn('mediaelementError: '+ message);
		setTimeout(function(){
			if($(elem).data('mediaerror')){
				$(elem).trigger('mediaerror');
			}
		}, 1);
	};
	
	var handleSWF = (function(){
		var requested;
		return function( mediaElem, ret, data ){
			webshims.ready('mediaelement-swf', function(){
				if(mediaelement.createSWF){
					mediaelement.createSWF( mediaElem, ret, data );
				} else if(!requested) {
					requested = true;
					loadSwf();
					//readd to ready
					handleSWF( mediaElem, ret, data );
				}
			});
		};
	})();
	
	var stepSources = function(elem, data, useSwf, _srces, _noLoop){
		var ret;
		if(useSwf || (useSwf !== false && data && data.isActive == 'flash')){
			ret = mediaelement.canSwfPlaySrces(elem, _srces);
			if(!ret){
				if(_noLoop){
					mediaelement.setError(elem, false);
				} else {
					stepSources(elem, data, false, _srces, true);
				}
			} else {
				handleSWF(elem, ret, data);
			}
		} else {
			ret = mediaelement.canNativePlaySrces(elem, _srces);
			if(!ret){
				if(_noLoop){
					mediaelement.setError(elem, false);
				} else {
					stepSources(elem, data, true, _srces, true);
				}
			} else if(data && data.isActive == 'flash') {
				mediaelement.setActive(elem, 'html5', data);
			}
		}
	};
	var stopParent = /^(?:embed|object)$/i;
	var selectSource = function(elem, data){
		var baseData = webshims.data(elem, 'mediaelementBase') || webshims.data(elem, 'mediaelementBase', {});
		var _srces = mediaelement.srces(elem);
		var parent = elem.parentNode;
		
		clearTimeout(baseData.loadTimer);
		$.data(elem, 'mediaerror', false);
		
		if(!_srces.length){return;}
		if(!parent || stopParent.test(parent.nodeName || '')){return;}
		data = data || webshims.data(elem, 'mediaelement');
		stepSources(elem, data, options.preferFlash || undefined, _srces);
	};
	
	
	$(document).bind('ended', function(e){
		var data = webshims.data(e.target, 'mediaelement');
		if( supportsLoop && (!data || data.isActive == 'html5') && !$.prop(e.target, 'loop')){return;}
		setTimeout(function(){
			if( $.prop(e.target, 'paused') || !$.prop(e.target, 'loop') ){return;}
			$(e.target).prop('currentTime', 0).play();
		}, 1);
		
	});
	if(!supportsLoop){
		webshims.defineNodeNamesBooleanProperty(['audio', 'video'], 'loop');
	}
	
	['audio', 'video'].forEach(function(nodeName){
		var supLoad = webshims.defineNodeNameProperty(nodeName, 'load',  {
			prop: {
				value: function(){
					var data = webshims.data(this, 'mediaelement');
					selectSource(this, data);
					if(hasNative && (!data || data.isActive == 'html5') && supLoad.prop._supvalue){
						supLoad.prop._supvalue.apply(this, arguments);
					}
				}
			}
		});
		nativeCanPlayType[nodeName] = webshims.defineNodeNameProperty(nodeName, 'canPlayType',  {
			prop: {
				value: function(type){
					var ret = '';
					if(hasNative && nativeCanPlayType[nodeName].prop._supvalue){
						ret = nativeCanPlayType[nodeName].prop._supvalue.call(this, type);
						if(ret == 'no'){
							ret = '';
						}
					}
					if(!ret && hasSwf){
						type = $.trim((type || '').split(';')[0]);
						if(mediaelement.swfMimeTypes.indexOf(type) != -1){
							ret = 'maybe';
						}
					}
					return ret;
				}
			}
		});
	});
	webshims.onNodeNamesPropertyModify(['audio', 'video'], ['src', 'poster'], {
		set: function(){
			var elem = this;
			var baseData = webshims.data(elem, 'mediaelementBase') || webshims.data(elem, 'mediaelementBase', {});
			clearTimeout(baseData.loadTimer);
			baseData.loadTimer = setTimeout(function(){
				selectSource(elem);
				elem = null;
			}, 9);
		}
	});
	
	
	//init
	webshims.addReady(function(context, insertedElement){
		$('video, audio', context)
			.add(insertedElement.filter('video, audio'))
			.each(function(){
				selectSource(this);
			})
		;
	 });	
	webshims.isReady('mediaelement-core', true);
});
})(jQuery, Modernizr, jQuery.webshims);