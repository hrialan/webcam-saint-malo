
    <!doctype html>
    <html lang="fr">
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-168995651-1"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'UA-168995651-1');
        </script>

        <script data-ad-client="ca-pub-8712822764035382" async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>


        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">

        <meta name="apple-mobile-web-app-title" content="Webcam Saint-Malo">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <link rel="apple-touch-icon-precomposed" href="/apple-touch-icon-152x152-precomposed.jpg" sizes="152x152">
        <link rel="apple-touch-icon-precomposed" href="/apple-touch-icon-120x120-precomposed.jpg" sizes="120x120">
        <link rel="apple-touch-icon-precomposed" href="/apple-touch-icon-76x76-precomposed.jpg" sizes="76x76">
        <link rel="apple-touch-icon-precomposed" href="/apple-touch-icon-precomposed.jpg">
        <link rel="apple-touch-icon" href="/apple-touch-icon-152x152-precomposed.jpg" sizes="152x152">

       <meta charset="utf-8">
        <title>Webcam Saint-Malo</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>

    <div class="main_container">


        <div class="quarter">
            <div class="video-container">
                <iframe width="560" height="315" src="https://www.youtube.com/embed/OetL01QjfBs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>            </div>
        </div>

        <div class="quarter">
            <div class="video-container">
                <iframe width="560" height="315" src="https://www.youtube.com/embed/2uznaTjvb7I"
                        frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen></iframe>
            </div>
        </div>

        <div class="quarter">
            <div class="video-container">
                <iframe width="560" height="315" src="https://www.youtube.com/embed/p6nAlz4_bdI"
                        frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen></iframe>
            </div>
        </div>
        <div class="quarter">
            <div class="video-container">
                <?php
                if(isset($_GET['action'])){

                    if ($_GET['action'] == 'meteo') {
                        ?>


                        <iframe width="560" height="315"
                                src="https://embed.windy.com/embed2.html?lat=48.074&lon=-2.613&zoom=7&level=surface&overlay=wind&menu=&message=&marker=&calendar=&pressure=&type=map&location=coordinates&detail=true&detailLat=48.650&detailLon=-2.020&metricWind=default&metricTemp=default&radarRange=-1"
                                frameborder="0"></iframe>


                    <?php
                    } elseif ($_GET['action'] == 'marinetraffic'){
                    ?>

                        <script type="text/javascript">
                            width = '100%';		// the width of the embedded map in pixels or percentage
                            height = '450';		// the height of the embedded map in pixels or percentage
                            border = '0';		// the width of the border around the map (zero means no border)
                            shownames = 'false';	// to display ship names on the map (true or false)
                            latitude = '48.6493';	// the latitude of the center of the map, in decimal degrees
                            longitude = '-2.0257';	// the longitude of the center of the map, in decimal degrees
                            zoom = '13';		// the zoom level of the map (values between 2 and 17)
                            maptype = '0';		// use 0 for Normal Map, 1 for Satellite
                            trackvessel = '0';	// MMSI of a vessel (note: vessel will be displayed only if within range of the system) - overrides "zoom" option
                            fleet = '';		// the registered email address of a user-defined fleet (user's default fleet is used)
                        </script>
                        <script type="text/javascript" src="//www.marinetraffic.com/js/embed.js"></script>


                        <?php
                    } elseif ($_GET['action'] == 'webcam_beaufort'){
                        ?>
                        <div class="video-container">
                                <iframe width="560" height="315" frameborder="0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                                        allowfullscreen src="https://www.vision-environnement.com/live/player/beaufort0.php"></iframe>
                        </div>

                        <?php
                    } elseif ($_GET['action'] == 'arcachon' or $_GET['action'] == 'beyond' ){
                        ?>
                        <div class="video-container">
                                <iframe width="560" height="315" frameborder="0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                                        allowfullscreen src="https://pv.viewsurf.com/1242/Arcachon-Jetee-Thiers-Live"></iframe>
                        </div>
                        <?php
                    }else{
                        echo '<p class="warning">Action inconnue</p>';
                    }
                }else
                {
                    echo '<p class="warning">Aucune action prise en compte</p>';
                }
                ?>

            </div>
        </div>
        <?php
        if ($_GET['action'] == 'beyond'){
        ?>

        <div id="marine_traffic_bottom">
            <script type="text/javascript">
                width = '100%';		// the width of the embedded map in pixels or percentage
                height = '310';		// the height of the embedded map in pixels or percentage
                border = '0';		// the width of the border around the map (zero means no border)
                shownames = 'false';	// to display ship names on the map (true or false)
                latitude = '48.6493';	// the latitude of the center of the map, in decimal degrees
                longitude = '-2.0257';	// the longitude of the center of the map, in decimal degrees
                zoom = '13';		// the zoom level of the map (values between 2 and 17)
                maptype = '0';		// use 0 for Normal Map, 1 for Satellite
                trackvessel = '0';	// MMSI of a vessel (note: vessel will be displayed only if within range of the system) - overrides "zoom" option
                fleet = '';		// the registered email address of a user-defined fleet (user's default fleet is used)
            </script>
            <script type="text/javascript" src="//www.marinetraffic.com/js/embed.js"></script>

        </div>
        <?php
        }
        else {
            echo '';
            }
        ?>
    </div>
    <footer>
            <p class="copy">&copy; 2020 Hugo Rialan / hugo.rialan@gmail.com<p>
            <nav>
<!--                <a href="webcam.php?action=meteo">Météo</a>-->
                <a href="webcam.php?action=marinetraffic">Marine-Traffic</a>
                <a href="webcam.php?action=webcam_beaufort">Hotel-Beaufort</a>
            </nav>
    </footer>

    <script>

    </script>
    </body>
    </html>

