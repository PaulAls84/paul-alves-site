<?php
/**
 * Article de blog (reprend src/pages/[slug].astro).
 */

defined( 'ABSPATH' ) || exit;

get_header();

while ( have_posts() ) :
	the_post();
	$post_id = get_the_ID();
	$cat     = pa_post_category( $post_id );
	$cover   = pa_cover_url( $post_id, 'large' );
	$url     = get_permalink();
	$title   = get_the_title();
	$share   = array(
		'twitter'  => 'https://twitter.com/intent/tweet?text=' . rawurlencode( $title ) . '&url=' . rawurlencode( $url ),
		'linkedin' => 'https://www.linkedin.com/sharing/share-offsite/?url=' . rawurlencode( $url ),
		'facebook' => 'https://www.facebook.com/sharer/sharer.php?u=' . rawurlencode( $url ),
		'whatsapp' => 'https://api.whatsapp.com/send?text=' . rawurlencode( $title ) . '%20' . rawurlencode( $url ),
	);
	?>

	<section class="article-hero">
		<?php if ( $cover ) : ?>
			<div class="hero-bg">
				<img src="<?php echo esc_url( $cover ); ?>" alt="" role="presentation" width="1200" height="630" fetchpriority="high" decoding="async" />
			</div>
		<?php endif; ?>
		<div class="hero-overlay"></div>
		<div class="wrap hero-content">
			<p class="eyebrow" style="text-align:left;">
				<?php if ( $cat ) : ?>
					<a href="<?php echo esc_url( get_category_link( $cat ) ); ?>" class="eyebrow-link"><?php echo esc_html( $cat->name ); ?></a>
				<?php else : ?>
					Blog
				<?php endif; ?>
			</p>
			<h1><?php the_title(); ?></h1>
			<p class="lede"><?php echo esc_html( get_the_excerpt() ); ?></p>
			<div class="article-meta">
				<span class="item"><?php echo pa_svg( 'calendar' ); // phpcs:ignore ?> <?php echo esc_html( get_the_date( 'j F Y' ) ); ?></span>
				<span class="item"><?php echo pa_svg( 'user' ); // phpcs:ignore ?> Paul Alves</span>
			</div>
		</div>
	</section>

	<div class="article-layout">
		<aside class="article-toc" id="articleToc" aria-label="Sommaire de l'article">
			<p class="toc-title">
				<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="15" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
				Sommaire
			</p>
			<ol class="toc-list" id="tocList"></ol>
		</aside>

		<div class="article-body">
			<article class="article-content">
				<?php the_content(); ?>
			</article>

			<div class="share-section">
				<p class="share-label">Partager cet article</p>
				<div class="share-buttons">
					<a href="<?php echo esc_url( $share['twitter'] ); ?>" rel="nofollow noopener noreferrer" target="_blank" class="share-btn share-btn--twitter" aria-label="Partager sur X (Twitter)">
						<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.748l7.73-8.835L1.254 2.25H8.08l4.26 5.632 5.905-5.632zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
						X
					</a>
					<a href="<?php echo esc_url( $share['linkedin'] ); ?>" rel="nofollow noopener noreferrer" target="_blank" class="share-btn share-btn--linkedin" aria-label="Partager sur LinkedIn">
						<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/></svg>
						LinkedIn
					</a>
					<a href="<?php echo esc_url( $share['facebook'] ); ?>" rel="nofollow noopener noreferrer" target="_blank" class="share-btn share-btn--facebook" aria-label="Partager sur Facebook">
						<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
						Facebook
					</a>
					<a href="<?php echo esc_url( $share['whatsapp'] ); ?>" rel="nofollow noopener noreferrer" target="_blank" class="share-btn share-btn--whatsapp" aria-label="Partager sur WhatsApp">
						<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.127.558 4.122 1.528 5.857L.057 23.12a.75.75 0 0 0 .923.899l5.356-1.538A11.943 11.943 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22.5c-1.92 0-3.735-.51-5.295-1.395l-.39-.226-3.812 1.095 1.038-3.71-.247-.403A10.44 10.44 0 0 1 1.5 12C1.5 6.201 6.201 1.5 12 1.5S22.5 6.201 22.5 12 17.799 22.5 12 22.5z"/></svg>
						WhatsApp
					</a>
					<button class="share-btn share-btn--copy" id="copyBtn" aria-label="Copier le lien">
						<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
						<span id="copyLabel">Copier le lien</span>
					</button>
				</div>
			</div>

			<div class="article-footer-nav">
				<a href="<?php echo esc_url( home_url( '/blog/' ) ); ?>" class="btn btn-outline" style="font-size: 13px; padding: 10px 18px;">← Tous les articles</a>
				<a href="#" <?php echo pa_cal_attrs(); // phpcs:ignore ?> class="btn btn-gold" style="font-size: 13px; padding: 10px 18px;">Travaillons ensemble</a>
			</div>
		</div>
	</div>

	<?php
	// Articles similaires : même catégorie d'abord, puis les autres.
	$same    = $cat ? get_posts( array( 'numberposts' => 3, 'category' => $cat->term_id, 'post__not_in' => array( $post_id ) ) ) : array();
	$related = $same;
	if ( count( $related ) < 3 ) {
		$related = array_merge( $related, get_posts( array(
			'numberposts'  => 3 - count( $related ),
			'post__not_in' => array_merge( array( $post_id ), wp_list_pluck( $related, 'ID' ) ),
		) ) );
	}
	if ( $related ) :
		?>
		<section class="related-section">
			<div class="wrap">
				<p class="section-eyebrow">Continuer la lecture</p>
				<h2 class="section-title">Articles <span class="accent">similaires</span></h2>
				<div class="related-grid">
					<?php foreach ( $related as $p ) : $pc = pa_post_category( $p->ID ); $img = pa_cover_url( $p->ID, 'medium_large' ); ?>
						<a href="<?php echo esc_url( get_permalink( $p ) ); ?>" class="related-card">
							<div class="related-card-img">
								<?php if ( $img ) : ?>
									<img src="<?php echo esc_url( $img ); ?>" alt="<?php echo esc_attr( get_the_title( $p ) ); ?>" width="400" height="220" loading="lazy" />
								<?php else : ?>
									<div class="related-card-placeholder"></div>
								<?php endif; ?>
							</div>
							<div class="related-card-body">
								<?php if ( $pc ) : ?><span class="related-cat"><?php echo esc_html( $pc->name ); ?></span><?php endif; ?>
								<h3><?php echo esc_html( get_the_title( $p ) ); ?></h3>
								<p><?php echo esc_html( get_the_excerpt( $p ) ); ?></p>
								<span class="related-link">Lire l'article →</span>
							</div>
						</a>
					<?php endforeach; ?>
				</div>
			</div>
		</section>
	<?php endif; ?>

	<?php echo pa_cta_band_html(); // phpcs:ignore ?>

<?php
endwhile;

get_footer();
