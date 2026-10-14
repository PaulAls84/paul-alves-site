<?php
/**
 * Fonctions utilitaires partagées par les modèles et les shortcodes.
 */

defined( 'ABSPATH' ) || exit;

/**
 * URL d'une image du site. Les logos et l'image par défaut des articles sont
 * dans la médiathèque (ids ci-dessous) ; à défaut, on cherche dans assets/img.
 */
function pa_asset_url( $file ) {
	$media = array(
		'logo-wordmark.webp'    => 57,
		'logo-mark.png'         => 56,
		'logo-full.png'         => 58,
		'blog-placeholder.webp' => 48,
	);
	if ( isset( $media[ $file ] ) ) {
		$url = wp_get_attachment_url( $media[ $file ] );
		if ( $url ) {
			return $url;
		}
	}
	return get_stylesheet_directory_uri() . '/assets/img/' . $file;
}

/** Attributs de la popup Cal.com (prise de rendez-vous). */
function pa_cal_attrs() {
	return sprintf(
		'data-cal-link="%s" data-cal-namespace="%s" data-cal-config=\'{"layout":"month_view"}\'',
		esc_attr( PA_CAL_LINK ),
		esc_attr( PA_CAL_NS )
	);
}

/** Icônes SVG reprises du site Astro. */
function pa_svg( $name, $size = 16 ) {
	$s     = (int) $size;
	$open  = '<svg width="' . $s . '" height="' . $s . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">';
	$fill  = '<svg width="' . $s . '" height="' . $s . '" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">';
	$icons = array(
		'phone'    => $open . '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.37 1.9.72 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.35 1.85.59 2.81.72A2 2 0 0 1 22 16.92z"/></svg>',
		'mail'     => $open . '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg>',
		'pin'      => $open . '<path d="M20 10c0 7-8 12-8 12s-8-5-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
		'calendar' => $open . '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
		'user'     => $open . '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg>',
		'linkedin' => $fill . '<path d="M20.5 2h-17A1.5 1.5 0 0 0 2 3.5v17A1.5 1.5 0 0 0 3.5 22h17a1.5 1.5 0 0 0 1.5-1.5v-17A1.5 1.5 0 0 0 20.5 2zM8 19H5v-9h3zM6.5 8.25A1.75 1.75 0 1 1 8.3 6.5a1.78 1.78 0 0 1-1.8 1.75zM19 19h-3v-4.74c0-1.42-.6-1.93-1.38-1.93A1.74 1.74 0 0 0 13 14.19a.66.66 0 0 0 0 .14V19h-3v-9h2.9v1.3a3.11 3.11 0 0 1 2.7-1.4c1.55 0 3.36.86 3.36 3.66z"/></svg>',
		'x'        => $fill . '<path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>',
		'github'   => $fill . '<path d="M12 0a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2.2c-3.3.7-4-1.4-4-1.4-.6-1.4-1.4-1.8-1.4-1.8-1.1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 0z"/></svg>',
		'agenda'   => '<svg width="' . $s . '" height="' . $s . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"/></svg>',
	);
	return $icons[ $name ] ?? '';
}

/** Image de couverture d'un article, en version WebP si elle existe. */
function pa_cover_url( $post_id, $size = 'large' ) {
	$id = get_post_thumbnail_id( $post_id );
	if ( ! $id ) {
		return '';
	}
	$src = wp_get_attachment_image_url( $id, $size );
	return $src ? $src : '';
}

/** Nom de la (première) catégorie d'un article. */
function pa_post_category( $post_id ) {
	$cats = get_the_category( $post_id );
	return $cats ? $cats[0] : null;
}

/** Carte d'article (grilles du blog, de l'accueil et des catégories). */
function pa_post_card( $post, $index = 99 ) {
	$post  = get_post( $post );
	$cat   = pa_post_category( $post->ID );
	$img   = pa_cover_url( $post->ID, 'medium_large' );
	$title = get_the_title( $post );
	$load  = $index < 2 ? 'eager' : 'lazy';
	$prio  = 0 === $index ? ' fetchpriority="high"' : '';
	ob_start();
	?>
	<a href="<?php echo esc_url( get_permalink( $post ) ); ?>" class="blog-card">
		<div class="blog-card-img">
			<img src="<?php echo esc_url( $img ? $img : pa_asset_url( 'blog-placeholder.webp' ) ); ?>" alt="<?php echo esc_attr( $title ); ?>" width="400" height="225" loading="<?php echo esc_attr( $load ); ?>"<?php echo $prio; // phpcs:ignore ?> decoding="async" />
		</div>
		<div class="blog-card-meta">
			<?php if ( $cat ) : ?><span class="blog-cat"><?php echo esc_html( $cat->name ); ?></span><?php endif; ?>
			<span class="blog-date"><?php echo esc_html( get_the_date( 'j F Y', $post ) ); ?></span>
		</div>
		<h3><?php echo esc_html( $title ); ?></h3>
		<p><?php echo esc_html( get_the_excerpt( $post ) ); ?></p>
		<span class="blog-link">Lire l'article &nbsp;→</span>
	</a>
	<?php
	return ob_get_clean();
}

/** Filtres par catégorie du blog. */
function pa_category_nav( $active_slug = null ) {
	$cats = get_categories( array( 'hide_empty' => true, 'exclude' => array( (int) get_option( 'default_category' ) ) ) );
	$blog = get_option( 'page_for_posts' ) ? get_permalink( get_option( 'page_for_posts' ) ) : home_url( '/blog/' );
	$out  = '<nav class="cat-nav" aria-label="Catégories du blog">';
	$out .= '<a href="' . esc_url( $blog ) . '" class="cat-chip ' . ( null === $active_slug ? 'is-active' : '' ) . '">Tous</a>';
	foreach ( $cats as $c ) {
		$out .= '<a href="' . esc_url( get_category_link( $c ) ) . '" class="cat-chip ' . ( $active_slug === $c->slug ? 'is-active' : '' ) . '">' . esc_html( $c->name ) . '</a>';
	}
	return $out . '</nav>';
}

/** Lien de navigation avec classe active. */
function pa_nav_link( $href, $label, $active ) {
	return '<a href="' . esc_url( $href ) . '"' . ( $active ? ' class="active"' : '' ) . '>' . esc_html( $label ) . '</a>';
}
