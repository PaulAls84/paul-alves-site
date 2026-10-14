<?php
/**
 * Shortcodes utilisés dans les pages Elementor (widget « Code court »).
 *
 * [pa_derniers_articles nombre="3"]  Derniers articles (accueil)
 * [pa_newsletter]                   Bloc d'inscription à la newsletter
 * [pa_cta_band]                     Bandeau « Prêt à faire décoller votre projet ? »
 * [pa_contact_form]                 Formulaire de contact
 * [pa_plan_du_site]                 Grille du plan du site
 */

defined( 'ABSPATH' ) || exit;

/* Derniers articles : « À la une » (épinglés) d'abord, puis les plus récents. */
add_shortcode( 'pa_derniers_articles', function ( $atts ) {
	$atts   = shortcode_atts( array( 'nombre' => 3 ), $atts );
	$n      = max( 1, (int) $atts['nombre'] );
	$sticky = get_option( 'sticky_posts', array() );
	$posts  = array();
	if ( $sticky ) {
		$posts = get_posts( array( 'post__in' => $sticky, 'numberposts' => $n, 'orderby' => 'date' ) );
	}
	if ( count( $posts ) < $n ) {
		$posts = array_merge( $posts, get_posts( array(
			'numberposts'  => $n - count( $posts ),
			'post__not_in' => wp_list_pluck( $posts, 'ID' ),
		) ) );
	}
	if ( ! $posts ) {
		return '';
	}
	$blog = get_option( 'page_for_posts' ) ? get_permalink( get_option( 'page_for_posts' ) ) : home_url( '/blog/' );
	$out  = '<div class="blog-grid">';
	foreach ( $posts as $i => $p ) {
		$out .= pa_post_card( $p, 99 );
	}
	$out .= '</div><div class="blog-center"><a href="' . esc_url( $blog ) . '" class="btn btn-outline">Voir tous les articles</a></div>';
	return $out;
} );

/* Newsletter (inscription Systeme.io via l'API REST du thème). */
function pa_newsletter_html() {
	ob_start();
	?>
	<section class="newsletter">
		<div class="wrap">
			<p class="section-eyebrow">Newsletter</p>
			<h2 class="section-title">Conseils SEO &amp; Web directement dans votre <span class="accent">boîte mail</span></h2>
			<div class="newsletter-inner">
				<p>Recevez mes conseils en développement web et référencement naturel : des retours d'expérience concrets, sans jargon, et pas de spam.</p>
				<form class="newsletter-form" data-pa-newsletter novalidate>
					<input type="email" name="email" placeholder="Votre adresse email" required autocomplete="email" />
					<button type="submit" class="btn btn-gold">
						<span class="btn-label">S'inscrire gratuitement</span>
						<span class="btn-loading" style="display:none">Inscription…</span>
					</button>
				</form>
				<p class="newsletter-notice" style="display:none; margin-top: 12px; font-size: 14px;"></p>
			</div>
		</div>
	</section>
	<?php
	return ob_get_clean();
}
add_shortcode( 'pa_newsletter', 'pa_newsletter_html' );

/* Bandeau d'appel à l'action (prise de rendez-vous). */
function pa_cta_band_html() {
	ob_start();
	?>
	<section class="cta-band" id="contact">
		<div class="wrap">
			<div class="cta-band-inner">
				<div class="cta-icon"><?php echo pa_svg( 'agenda', 28 ); // phpcs:ignore ?></div>
				<div>
					<h3>Prêt à faire décoller votre projet ?</h3>
					<p>Réservez un appel gratuit de 30 minutes pour discuter de vos objectifs.</p>
				</div>
				<a href="#" <?php echo pa_cal_attrs(); // phpcs:ignore ?> class="btn btn-gold">Réserver un appel gratuit</a>
			</div>
		</div>
	</section>
	<?php
	return ob_get_clean();
}
add_shortcode( 'pa_cta_band', 'pa_cta_band_html' );

/* Formulaire de contact (envoi via l'API REST du thème). */
add_shortcode( 'pa_contact_form', function () {
	$sujets = array(
		'Création de site WordPress',
		'Refonte de site existant',
		'Optimisation SEO',
		'Optimisation des performances',
		'Maintenance mensuelle',
		'Autre demande',
	);
	ob_start();
	?>
	<div class="contact-form-wrap">
		<form id="contactForm" class="contact-form" novalidate>
			<div class="form-row form-row--2">
				<div class="field">
					<label for="nom">Nom complet <span class="req">*</span></label>
					<input type="text" id="nom" name="nom" placeholder="Marie Dupont" required />
				</div>
				<div class="field">
					<label for="email">Email <span class="req">*</span></label>
					<input type="email" id="email" name="email" placeholder="marie@exemple.fr" required />
				</div>
			</div>
			<div class="form-row form-row--2">
				<div class="field">
					<label for="telephone">Téléphone <span class="opt">(optionnel)</span></label>
					<input type="tel" id="telephone" name="telephone" placeholder="06 XX XX XX XX" />
				</div>
				<div class="field">
					<label for="sujet">Sujet <span class="req">*</span></label>
					<select id="sujet" name="sujet" required>
						<option value="" disabled selected>Choisissez un sujet</option>
						<?php foreach ( $sujets as $s ) : ?>
							<option value="<?php echo esc_attr( $s ); ?>"><?php echo esc_html( $s ); ?></option>
						<?php endforeach; ?>
					</select>
				</div>
			</div>
			<div class="field">
				<label for="message">Votre message <span class="req">*</span></label>
				<textarea id="message" name="message" rows="6" placeholder="Décrivez votre projet en quelques lignes : contexte, objectifs, délais…" required></textarea>
			</div>
			<!-- Piège à robots : champ invisible qui doit rester vide -->
			<div style="position:absolute;left:-9999px" aria-hidden="true"><input type="text" name="site_web" tabindex="-1" autocomplete="off" /></div>
			<div id="formMsg" class="form-msg" aria-live="polite"></div>
			<button type="submit" class="btn btn-gold submit-btn" id="submitBtn">
				<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
				Envoyer le message
			</button>
		</form>
	</div>
	<?php
	return ob_get_clean();
} );

/* Plan du site : pages principales, blog (catégories + articles), pages légales. */
add_shortcode( 'pa_plan_du_site', function () {
	$icon = function ( $paths ) {
		return '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">' . $paths . '</svg>';
	};
	$blog_links = array( array( home_url( '/blog/' ), 'Accueil du blog', 'Tous les articles' ) );
	foreach ( get_categories( array( 'hide_empty' => true, 'exclude' => array( (int) get_option( 'default_category' ) ) ) ) as $c ) {
		$blog_links[] = array( get_category_link( $c ), 'Catégorie ' . $c->name, 'Articles ' . $c->name );
	}
	foreach ( get_posts( array( 'numberposts' => -1 ) ) as $p ) {
		$cat          = pa_post_category( $p->ID );
		$blog_links[] = array( get_permalink( $p ), get_the_title( $p ), $cat ? $cat->name : '' );
	}
	$sections = array(
		array(
			'Pages principales',
			$icon( '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>' ),
			array(
				array( home_url( '/' ), 'Accueil', 'Présentation, services, parcours' ),
				array( home_url( '/services/' ), 'Services', '6 prestations WordPress & SEO avec tarifs' ),
				array( home_url( '/a-propos/' ), 'À propos', 'Mon parcours et ma philosophie' ),
				array( home_url( '/realisations/' ), 'Réalisations', 'Projets clients et résultats' ),
				array( home_url( '/contact/' ), 'Contact', 'Formulaire, coordonnées, prise de rendez-vous' ),
			),
		),
		array(
			'Blog',
			$icon( '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>' ),
			$blog_links,
		),
		array(
			'Légal & informations',
			$icon( '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>' ),
			array(
				array( home_url( '/mentions-legales/' ), 'Mentions légales', 'Éditeur, hébergeur, SIREN' ),
				array( home_url( '/politique-confidentialite/' ), 'Politique de confidentialité', 'RGPD, cookies, vos droits' ),
				array( home_url( '/plan-du-site/' ), 'Plan du site', 'La page que vous lisez actuellement' ),
			),
		),
	);
	$out = '<div class="sitemap-grid">';
	foreach ( $sections as $s ) {
		$out .= '<div class="sitemap-section"><div class="sm-head"><div class="sm-icon">' . $s[1] . '</div><h2>' . esc_html( $s[0] ) . '</h2></div><ul class="sm-list">';
		foreach ( $s[2] as $l ) {
			$out .= '<li><a href="' . esc_url( $l[0] ) . '"><span class="sm-label">' . esc_html( $l[1] ) . '</span>';
			$out .= $l[2] ? '<span class="sm-desc">' . esc_html( $l[2] ) . '</span>' : '';
			$out .= '</a></li>';
		}
		$out .= '</ul></div>';
	}
	return $out . '</div>';
} );
