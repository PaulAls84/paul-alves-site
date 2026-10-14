<?php
/**
 * Thème enfant paul-alves.fr
 *
 * Reprend le site Astro : en-tête, pied de page, articles, blog et catégories
 * sont rendus par le thème ; les pages (accueil, services…) sont construites
 * avec Elementor et réutilisent les mêmes classes CSS.
 */

defined( 'ABSPATH' ) || exit;

define( 'PA_VERSION', '1.1.3' );
define( 'PA_PROD_HOST', 'paul-alves.fr' );
define( 'PA_GA_ID', 'G-1LX7VWG6KW' );
define( 'PA_CAL_LINK', 'paul-alves/audit-offert' );
define( 'PA_CAL_NS', 'audit-offert' );
define( 'PA_PHONE', '+33656666684' );
define( 'PA_PHONE_DISPLAY', '06 56 66 66 84' );
define( 'PA_EMAIL', 'contact@paul-alves.fr' );

require_once __DIR__ . '/inc/helpers.php';
require_once __DIR__ . '/inc/shortcodes.php';
require_once __DIR__ . '/inc/rest.php';
require_once __DIR__ . '/inc/seo.php';

/** Site de production ? (GA4, indexation) */
function pa_is_prod() {
	$host = wp_parse_url( home_url(), PHP_URL_HOST );
	return in_array( $host, array( PA_PROD_HOST, 'www.' . PA_PROD_HOST ), true );
}

/* ------------------------------------------------------------------------
 * Styles et scripts
 * --------------------------------------------------------------------- */

// Le design complet est dans site.css : on retire les feuilles de Hello.
add_filter( 'hello_elementor_enqueue_style', '__return_false' );
add_filter( 'hello_elementor_enqueue_theme_style', '__return_false' );

add_action( 'wp_enqueue_scripts', function () {
	foreach ( array( 'hello-elementor', 'hello-elementor-theme-style', 'hello-elementor-header-footer', 'hello-elementor-child-style' ) as $h ) {
		wp_dequeue_style( $h );
	}

	wp_enqueue_style(
		'pa-fonts',
		'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap',
		array(),
		null
	);

	// Chargé après Elementor pour que les règles du site l'emportent à spécificité égale.
	$deps = wp_style_is( 'elementor-frontend', 'registered' ) ? array( 'elementor-frontend' ) : array();
	$css  = get_stylesheet_directory() . '/assets/css/site.css';
	wp_enqueue_style( 'pa-site', get_stylesheet_directory_uri() . '/assets/css/site.css', $deps, filemtime( $css ) );

	$js = get_stylesheet_directory() . '/assets/js/site.js';
	wp_enqueue_script( 'pa-site', get_stylesheet_directory_uri() . '/assets/js/site.js', array(), filemtime( $js ), array( 'in_footer' => true, 'strategy' => 'defer' ) );
	wp_localize_script( 'pa-site', 'PA', array(
		'rest'  => esc_url_raw( rest_url( 'pa/v1/' ) ),
		'calNs' => PA_CAL_NS,
	) );

	// Les styles des blocs ne servent qu'aux articles.
	if ( ! is_singular( 'post' ) ) {
		wp_dequeue_style( 'wp-block-library' );
		wp_dequeue_style( 'global-styles' );
		wp_dequeue_style( 'classic-theme-styles' );
	}
}, 20 );

add_action( 'wp_head', function () {
	echo '<link rel="preconnect" href="https://fonts.googleapis.com" />' . "\n";
	echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />' . "\n";
}, 1 );

// Favicon (logo-mark) si aucune icône n'est définie dans l'administration.
add_action( 'wp_head', function () {
	if ( ! has_site_icon() ) {
		echo '<link rel="icon" type="image/png" href="' . esc_url( pa_asset_url( 'logo-mark.png' ) ) . '" />' . "\n";
	}
}, 2 );

/* ------------------------------------------------------------------------
 * Classes de body : une classe par page pour les styles propres à la page
 * --------------------------------------------------------------------- */
add_filter( 'body_class', function ( $classes ) {
	if ( is_page() ) {
		$slug      = get_post_field( 'post_name', get_queried_object_id() );
		$classes[] = 'pa-' . $slug;
		if ( in_array( $slug, array( 'mentions-legales', 'politique-confidentialite' ), true ) ) {
			$classes[] = 'pa-legal';
		}
	}
	if ( is_front_page() ) {
		$classes[] = 'pa-accueil';
	}
	return $classes;
} );

/* ------------------------------------------------------------------------
 * Blog : tous les articles sur une seule page (comme le site Astro)
 * et catégories servies sous /blog/categorie/<slug>/
 * --------------------------------------------------------------------- */
add_action( 'pre_get_posts', function ( $q ) {
	if ( ! is_admin() && $q->is_main_query() && ( $q->is_home() || $q->is_category() ) ) {
		$q->set( 'posts_per_page', -1 );
		$q->set( 'ignore_sticky_posts', true );
	}
} );

add_action( 'init', function () {
	if ( 'blog/categorie' !== get_option( 'category_base' ) ) {
		update_option( 'category_base', 'blog/categorie' );
		flush_rewrite_rules( false );
	}
}, 99 );

/* ------------------------------------------------------------------------
 * Elementor : pas de couleurs ni de polices par défaut sur les widgets,
 * pour que les titres et textes héritent des styles du site.
 * --------------------------------------------------------------------- */
add_filter( 'pre_option_elementor_disable_color_schemes', function () { return 'yes'; } );
add_filter( 'pre_option_elementor_disable_typography_schemes', function () { return 'yes'; } );

/* ------------------------------------------------------------------------
 * Divers
 * --------------------------------------------------------------------- */
add_action( 'after_setup_theme', function () {
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'title-tag' );
	add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );
}, 20 );

// Pas d'emojis WordPress (scripts inutiles).
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
