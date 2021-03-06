    // Construct the viewer, with a high-res terrain source pre-selected.
    
var viewer= new Cesium.viewer('cesiumContainer');
    var camera = viewer.camera;
    var scene = viewer.scene;
    var globe = scene.globe;
    var ellipsoid = Cesium.Ellipsoid.WGS84;
    var geodesic = new Cesium.EllipsoidGeodesic();


    var tileset = scene.primitives.add(new Cesium.Cesium3DTileset({
      url: 'http://127.0.0.1:5000/static/a12/tileset.json'
    }));
    tileset.readyPromise.then(function() {
      // console.log(tileset);
      var boundingSphere = tileset.boundingSphere;
      camera.viewBoundingSphere(boundingSphere, new Cesium.HeadingPitchRange(0.5, -0.2, boundingSphere.radius * 4.0));
      camera.lookAtTransform(Cesium.Matrix4.IDENTITY);
    }).otherwise(function(error) {
      throw(error);
    });
    tileset.allTilesLoaded.addEventListener(function() {
      console.log('All tiles are loaded');
    });


    var points = scene.primitives.add(new Cesium.PointPrimitiveCollection());
    var point1, point2;
    var point1GeoPosition, point2GeoPosition;
    var polylines = scene.primitives.add(new Cesium.PolylineCollection());
    var polyline1, polyline2, polyline3;
    var distanceLabel, verticalLabel, horizontalLabel;
    var LINEPOINTCOLOR = Cesium.Color.RED;
    // var labels = scene.primitives.add(new Cesium.LabelCollection({scene: scene}));


    var label = {
      font : '14px monospace',
      showBackground : true,
      horizontalOrigin : Cesium.HorizontalOrigin.CENTER,
      verticalOrigin : Cesium.VerticalOrigin.CENTER,
      pixelOffset : new Cesium.Cartesian2(0, 0),
      eyeOffset: new Cesium.Cartesian3(0,0,-50),
      fillColor: Cesium.Color.WHITE,
    };

    function addDistanceLabel(point1, point2, height) {
      point1.cartographic = ellipsoid.cartesianToCartographic(point1.position);
      point2.cartographic = ellipsoid.cartesianToCartographic(point2.position);
      point1.longitude = parseFloat(Cesium.Math.toDegrees(point1.position.x));
      point1.latitude = parseFloat(Cesium.Math.toDegrees(point1.position.y));
      point2.longitude = parseFloat(Cesium.Math.toDegrees(point2.position.x));
      point2.latitude = parseFloat(Cesium.Math.toDegrees(point2.position.y));
      label.text = getHorizontalDistanceString(point1, point2);
      horizontalLabel = viewer.entities.add({
          position: getMidpoint(point1, point2, point1GeoPosition.height),
          label: label
      });
      label.text = getDistanceString(point1, point2);
      distanceLabel = viewer.entities.add({
          position: getMidpoint(point1, point2, height),
          label: label
      });
      label.text = getVerticalDistanceString();
      verticalLabel = viewer.entities.add({
          position: getMidpoint(point2, point2, height),
          label: label
      });
    };

    function getHorizontalDistanceString(point1, point2) {
      geodesic.setEndPoints(point1.cartographic, point2.cartographic);
      var meters = geodesic.surfaceDistance.toFixed(2);
      if (meters >= 1000) {
          return (meters / 1000).toFixed(1) + ' ????';
      }
      return meters + ' ??';
    };

    function getVerticalDistanceString() {
      var heights = [point1GeoPosition.height, point2GeoPosition.height];
      var meters = Math.max.apply(Math, heights) - Math.min.apply(Math, heights);
      if (meters >= 1000) {
          return (meters / 1000).toFixed(1) + ' ????';
      }
      return meters.toFixed(2) + ' ??';
    };

    function getDistanceString(point1, point2) {
      geodesic.setEndPoints(point1.cartographic, point2.cartographic);
      var horizontalMeters = geodesic.surfaceDistance.toFixed(2);
      var heights = [point1GeoPosition.height, point2GeoPosition.height];
      var verticalMeters = Math.max.apply(Math, heights) - Math.min.apply(Math, heights);
      var meters = Math.pow((Math.pow(horizontalMeters, 2) + Math.pow(verticalMeters, 2)), 0.5);

      if (meters >= 1000) {
          return (meters / 1000).toFixed(1) + ' ????';
      }
      return meters.toFixed(2) + ' ??';
    };

    function getMidpoint(point1, point2, height) {
      var scratch = new Cesium.Cartographic();
      geodesic.setEndPoints(point1.cartographic, point2.cartographic);
      var midpointCartographic = geodesic.interpolateUsingFraction(0.5, scratch);
      return Cesium.Cartesian3.fromRadians(midpointCartographic.longitude, midpointCartographic.latitude, height);
    };


    // Mouse over the globe to see the cartographic position
    var handler = new Cesium.ScreenSpaceEventHandler(scene.canvas);
    handler.setInputAction(function(click) {
        if (scene.mode !== Cesium.SceneMode.MORPHING) {
            var pickedObject = scene.pick(click.position);
            if (scene.pickPositionSupported && Cesium.defined(pickedObject)) {
                var cartesian = viewer.scene.pickPosition(click.position);
                // console.log(cartesian);
                if (Cesium.defined(cartesian)) {
                    if (points.length === 2) {
                        points.removeAll();
                        polylines.removeAll();
                        viewer.entities.remove(distanceLabel);
                        viewer.entities.remove(horizontalLabel);
                        viewer.entities.remove(verticalLabel);
                    }
                    //add first point
                    if (points.length === 0) {
                        point1 = points.add({
                            position : new Cesium.Cartesian3(cartesian.x, cartesian.y, cartesian.z),
                            color : LINEPOINTCOLOR
                        });
                    } //add second point and lines
                    else if (points.length === 1) {
                        point2 = points.add({
                            position : new Cesium.Cartesian3(cartesian.x, cartesian.y, cartesian.z),
                            color : LINEPOINTCOLOR
                        }); 
                        point1GeoPosition = Cesium.Cartographic.fromCartesian(point1.position);
                        point2GeoPosition = Cesium.Cartographic.fromCartesian(point2.position);
                        point3GeoPosition = Cesium.Cartographic.fromCartesian(new Cesium.Cartesian3(point2.position.x, point2.position.y, point1.position.z));  

                        var pl1Positions = [
                          new Cesium.Cartesian3.fromRadians(point1GeoPosition.longitude, point1GeoPosition.latitude, point1GeoPosition.height),
                          new Cesium.Cartesian3.fromRadians(point2GeoPosition.longitude, point2GeoPosition.latitude, point2GeoPosition.height)
                        ];
                        var pl2Positions = [
                          new Cesium.Cartesian3.fromRadians(point2GeoPosition.longitude, point2GeoPosition.latitude, point2GeoPosition.height),
                          new Cesium.Cartesian3.fromRadians(point2GeoPosition.longitude, point2GeoPosition.latitude, point1GeoPosition.height)
                        ];
                        var pl3Positions = [
                          new Cesium.Cartesian3.fromRadians(point1GeoPosition.longitude, point1GeoPosition.latitude, point1GeoPosition.height),
                          new Cesium.Cartesian3.fromRadians(point2GeoPosition.longitude, point2GeoPosition.latitude, point1GeoPosition.height)
                        ];

                        polyline1 = polylines.add({
                          show : true,
                          positions : pl1Positions,
                          width : 1,
                          material: new Cesium.Material({
                              fabric : {
                                  type : 'Color',
                                  uniforms : {
                                      color : LINEPOINTCOLOR
                                  }
                              }
                          })
                        }); 
                        polyline2 = polylines.add({
                          show : true,
                          positions : pl2Positions,
                          width : 1,
                          material: new Cesium.Material({
                              fabric : {
                                  type : 'PolylineDash',
                                  uniforms : {
                                      color : LINEPOINTCOLOR,
                                  }
                              },
                          })
                        });
                        polyline3 = polylines.add({
                          show : true,
                          positions : pl3Positions,
                          width : 1,
                          material: new Cesium.Material({
                              fabric : {
                                  type : 'PolylineDash',
                                  uniforms : {
                                      color : LINEPOINTCOLOR,
                                  }
                              },
                          })
                        }); 
                        var labelZ;
                        if (point2GeoPosition.height >= point1GeoPosition.height) {
                          labelZ = point1GeoPosition.height + (point2GeoPosition.height - point1GeoPosition.height)/2.0;
                        } else {
                          labelZ = point2GeoPosition.height + (point1GeoPosition.height - point2GeoPosition.height)/2.0;
                        };

                        addDistanceLabel(point1, point2, labelZ);

                    }
                }
            }
        }
    }, Cesium.ScreenSpaceEventType.LEFT_CLICK);