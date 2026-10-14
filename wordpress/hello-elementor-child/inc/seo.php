<?php
/**
 * SEO : indexation, GA4 (Consent Mode v2), données structurées, et champs
 * Rank Math exposés à l'API REST (pour les renseigner lors de la migration).
 */

defined( 'ABSPATH' ) || exit;

/* Préproduction : rien n'est indexé tant que le site n'est pas sur paul-alves.fr.
   La carte de contact (/qrcode/) n'est jamais indexée. */
function pa_noindex() {
	return ! pa_is_prod() || is_page( 'qrcode' );
}
add_filter( 'wp_robots', function ( $robots ) {
	if ( pa_noindex() ) {
		$robots['noindex']  = true;
		$robots['nofollow'] = true;
		unset( $robots['max-image-preview'] );
	}
	return $robots;
}, 999 );
add_filter( 'rank_math/frontend/robots', function ( $robots ) {
	if ( pa_noindex() ) {
		$robots['index']  = 'noindex';
		$robots['follow'] = 'nofollow';
	}
	return $robots;
}, 999 );

/* Titre et description Rank Math modifiables via l'API REST. */
add_action( 'init', function () {
	foreach ( array( 'post', 'page' ) as $type ) {
		foreach ( array( 'rank_math_title', 'rank_math_description', 'rank_math_focus_keyword' ) as $key ) {
			register_post_meta( $type, $key, array(
				'type'          => 'string',
				'single'        => true,
				'show_in_rest'  => true,
				'auth_callback' => function () {
					return current_user_can( 'edit_posts' );
				},
			) );
		}
	}
} );

/* GA4 avec Consent Mode v2 (tout refusé par défaut), uniquement en production.
   CookieYes met à jour le consentement quand le visiteur accepte. */
add_action( 'wp_head', function () {
	if ( ! pa_is_prod() || is_user_logged_in() ) {
		return;
	}
	?>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
window.gtag = gtag;
gtag('consent', 'default', {
  ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied',
  analytics_storage: 'denied', functionality_storage: 'granted', security_storage: 'granted',
  wait_for_update: 500
});
gtag('js', new Date());
gtag('config', '<?php echo esc_js( PA_GA_ID ); ?>');
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo esc_attr( PA_GA_ID ); ?>"></script>
	<?php
}, 1 );

/* Données structurées LocalBusiness + Person (toutes les pages, comme sur Astro). */
add_action( 'wp_head', function () {
	$site  = 'https://' . PA_PROD_HOST;
	$knows = array( 'WordPress', 'WooCommerce', 'SEO', 'Référencement naturel', 'Création de site web', 'Optimisation des performances web', 'Core Web Vitals', 'Google Search Console', 'Marketing de contenu' );
	$local = array(
		'@context'                  => 'https://schema.org',
		'@type'                     => array( 'LocalBusiness', 'ProfessionalService' ),
		'name'                      => 'Paul Alves',
		'description'               => 'Développeur Web & Consultant SEO freelance basé à Soissons. Création de sites WordPress sur mesure, refonte, optimisation SEO et performances. Disponible partout en France.',
		'url'                       => $site,
		'logo'                      => pa_asset_url( 'logo-full.png' ),
		'image'                     => pa_asset_url( 'logo-full.png' ),
		'email'                     => PA_EMAIL,
		'telephone'                 => PA_PHONE,
		'priceRange'                => '€€',
		'currenciesAccepted'        => 'EUR',
		'address'                   => array(
			'@type'           => 'PostalAddress',
			'streetAddress'   => '3 rue des Longues Raies',
			'postalCode'      => '02200',
			'addressLocality' => 'Soissons',
			'addressRegion'   => 'Hauts-de-France',
			'addressCountry'  => 'FR',
		),
		'geo'                       => array( '@type' => 'GeoCoordinates', 'latitude' => 49.3814, 'longitude' => 3.3236 ),
		'areaServed'                => array( '@type' => 'Country', 'name' => 'France' ),
		'knowsAbout'                => $knows,
		'openingHoursSpecification' => array( array(
			'@type'     => 'OpeningHoursSpecification',
			'dayOfWeek' => array( 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ),
			'opens'     => '09:00',
			'closes'    => '18:00',
		) ),
		'sameAs'                    => array( 'https://linkedin.com/in/paul-alves' ),
	);
	$person = array(
		'@context'    => 'https://schema.org',
		'@type'       => 'Person',
		'name'        => 'Paul Alves',
		'jobTitle'    => 'Développeur Web & Consultant SEO',
		'description' => "Freelance spécialisé WordPress et SEO. A généré plus d'un million de visiteurs organiques sur son propre blog avant d'accompagner les entreprises dans leur développement web et leur référencement.",
		'url'         => $site,
		'email'       => PA_EMAIL,
		'telephone'   => PA_PHONE,
		'address'     => array( '@type' => 'PostalAddress', 'addressLocality' => 'Soissons', 'addressRegion' => 'Hauts-de-France', 'addressCountry' => 'FR' ),
		'knowsAbout'  => $knows,
		'sameAs'      => array( 'https://linkedin.com/in/paul-alves' ),
		'worksFor'    => array( '@type' => 'Organization', 'name' => 'Paul Alves', 'url' => $site ),
	);
	foreach ( array( $local, $person ) as $data ) {
		echo '<script type="application/ld+json">' . wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
	}

	// FAQPage des articles : paires « **Question ?** réponse » de la section « FAQ ».
	if ( is_singular( 'post' ) ) {
		$html = apply_filters( 'the_content', get_post_field( 'post_content', get_queried_object_id() ) );
		if ( preg_match( '/<h2[^>]*>\s*FAQ\s*<\/h2>(.*?)(?=<h2|$)/s', $html, $m ) ) {
			$items = array();
			preg_match_all( '/<p[^>]*>\s*<strong>(.+?)<\/strong>\s*(.*?)<\/p>/s', $m[1], $pairs, PREG_SET_ORDER );
			foreach ( $pairs as $p ) {
				$q = trim( preg_replace( '/\s+/', ' ', wp_strip_all_tags( $p[1] ) ) );
				$a = trim( preg_replace( '/\s+/', ' ', wp_strip_all_tags( $p[2] ) ) );
				if ( $q && $a ) {
					$items[] = array( '@type' => 'Question', 'name' => html_entity_decode( $q ), 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => html_entity_decode( $a ) ) );
				}
			}
			if ( $items ) {
				echo '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => $items ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
			}
		}
	}
}, 5 );
