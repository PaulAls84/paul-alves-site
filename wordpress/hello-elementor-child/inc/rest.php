<?php
/**
 * API du site : formulaire de contact et newsletter (reprend /api/contact et
 * /api/newsletter du site Astro).
 *
 * Clés à déclarer dans wp-config.php :
 *   define( 'PA_SYSTEME_IO_API_KEY', '...' ); // newsletter + ajout des contacts
 *   define( 'PA_RESEND_API_KEY', '...' );     // optionnel : envoi via Resend,
 *                                             // sinon wp_mail() (SMTP du site)
 */

defined( 'ABSPATH' ) || exit;

add_action( 'rest_api_init', function () {
	register_rest_route( 'pa/v1', '/contact', array(
		'methods'             => 'POST',
		'callback'            => 'pa_rest_contact',
		'permission_callback' => '__return_true',
	) );
	register_rest_route( 'pa/v1', '/newsletter', array(
		'methods'             => 'POST',
		'callback'            => 'pa_rest_newsletter',
		'permission_callback' => '__return_true',
	) );
} );

/** Limite simple : 5 envois par IP et par tranche de 10 minutes. */
function pa_rate_limited( $action ) {
	$ip  = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '';
	$key = 'pa_rl_' . $action . '_' . md5( $ip );
	$n   = (int) get_transient( $key );
	if ( $n >= 5 ) {
		return true;
	}
	set_transient( $key, $n + 1, 10 * MINUTE_IN_SECONDS );
	return false;
}

/** Ajoute un contact dans Systeme.io (200 = déjà existant, 201 = créé). */
function pa_systeme_io_add( $payload ) {
	if ( ! defined( 'PA_SYSTEME_IO_API_KEY' ) || ! PA_SYSTEME_IO_API_KEY ) {
		return new WP_Error( 'config', 'Configuration manquante.' );
	}
	$res = wp_remote_post( 'https://api.systeme.io/api/contacts', array(
		'timeout' => 15,
		'headers' => array(
			'X-API-Key'    => PA_SYSTEME_IO_API_KEY,
			'Content-Type' => 'application/json',
			'accept'       => 'application/json',
		),
		'body'    => wp_json_encode( $payload ),
	) );
	if ( is_wp_error( $res ) ) {
		return $res;
	}
	$code = wp_remote_retrieve_response_code( $res );
	if ( 200 === $code || 201 === $code ) {
		return true;
	}
	error_log( '[pa] Systeme.io ' . $code . ' ' . wp_remote_retrieve_body( $res ) );
	return new WP_Error( 'systeme', 'Erreur lors de l\'inscription.' );
}

function pa_rest_newsletter( WP_REST_Request $req ) {
	$email = sanitize_email( (string) $req->get_param( 'email' ) );
	if ( ! is_email( $email ) ) {
		return new WP_REST_Response( array( 'error' => 'Adresse email invalide.' ), 400 );
	}
	if ( pa_rate_limited( 'nl' ) ) {
		return new WP_REST_Response( array( 'error' => 'Trop de tentatives, réessayez dans quelques minutes.' ), 429 );
	}
	$r = pa_systeme_io_add( array( 'email' => $email, 'tags' => array( array( 'name' => 'newsletter' ) ) ) );
	if ( is_wp_error( $r ) ) {
		$status = 'config' === $r->get_error_code() ? 500 : 502;
		return new WP_REST_Response( array( 'error' => $r->get_error_message() ), $status );
	}
	return new WP_REST_Response( array( 'success' => true ), 200 );
}

function pa_rest_contact( WP_REST_Request $req ) {
	$nom       = sanitize_text_field( (string) $req->get_param( 'nom' ) );
	$email     = sanitize_email( (string) $req->get_param( 'email' ) );
	$sujet     = sanitize_text_field( (string) $req->get_param( 'sujet' ) );
	$message   = sanitize_textarea_field( (string) $req->get_param( 'message' ) );
	$telephone = sanitize_text_field( (string) $req->get_param( 'telephone' ) );

	if ( '' !== (string) $req->get_param( 'site_web' ) ) {
		return new WP_REST_Response( array( 'success' => true ), 200 ); // robot : on ignore
	}
	if ( ! $nom || ! $email || ! $sujet || ! $message ) {
		return new WP_REST_Response( array( 'error' => 'Champs obligatoires manquants.' ), 400 );
	}
	if ( ! is_email( $email ) ) {
		return new WP_REST_Response( array( 'error' => 'Adresse email invalide.' ), 400 );
	}
	if ( pa_rate_limited( 'contact' ) ) {
		return new WP_REST_Response( array( 'error' => 'Trop de messages envoyés, réessayez dans quelques minutes.' ), 429 );
	}

	$to      = defined( 'PA_CONTACT_TO_EMAIL' ) ? PA_CONTACT_TO_EMAIL : PA_EMAIL;
	$from    = defined( 'PA_CONTACT_FROM_EMAIL' ) ? PA_CONTACT_FROM_EMAIL : PA_EMAIL;
	$subject = '[Contact] ' . $sujet . ' | ' . $nom;
	$e       = 'esc_html';
	$html    = '<div style="font-family:system-ui,-apple-system,Segoe UI,sans-serif;max-width:560px;margin:0 auto;padding:32px;color:#0a1d36;line-height:1.6;">'
		. '<div style="border-bottom:3px solid #d4a44a;padding-bottom:16px;margin-bottom:24px;"><h1 style="font-size:20px;margin:0;color:#0a1d36;">📩 Nouveau message du formulaire</h1>'
		. '<p style="margin:6px 0 0;font-size:13px;color:#6b7a8d;">paul-alves.fr / contact</p></div>'
		. '<table style="width:100%;border-collapse:collapse;font-size:14px;">'
		. '<tr><td style="padding:8px 0;color:#6b7a8d;width:120px;">De</td><td style="padding:8px 0;font-weight:600;">' . $e( $nom ) . '</td></tr>'
		. '<tr><td style="padding:8px 0;color:#6b7a8d;">Email</td><td style="padding:8px 0;"><a href="mailto:' . esc_attr( $email ) . '" style="color:#d4a44a;">' . $e( $email ) . '</a></td></tr>'
		. ( $telephone ? '<tr><td style="padding:8px 0;color:#6b7a8d;">Téléphone</td><td style="padding:8px 0;"><a href="tel:' . esc_attr( $telephone ) . '" style="color:#d4a44a;">' . $e( $telephone ) . '</a></td></tr>' : '' )
		. '<tr><td style="padding:8px 0;color:#6b7a8d;">Sujet</td><td style="padding:8px 0;font-weight:600;">' . $e( $sujet ) . '</td></tr></table>'
		. '<div style="margin-top:24px;padding:20px;background:#faf7f2;border-radius:10px;border-left:3px solid #d4a44a;">'
		. '<p style="margin:0 0 8px;font-size:12px;font-weight:700;color:#6b7a8d;text-transform:uppercase;letter-spacing:.08em;">Message</p>'
		. '<p style="margin:0;white-space:pre-wrap;color:#243a55;">' . $e( $message ) . '</p></div>'
		. '<p style="margin-top:32px;font-size:12px;color:#6b7a8d;border-top:1px solid #e6e0d4;padding-top:16px;">Pour répondre, clique simplement sur "Répondre" : la réponse partira directement à ' . $e( $email ) . '.</p></div>';
	$text = "Nouveau message du formulaire de contact | paul-alves.fr\n\nDe      : $nom\nEmail   : $email\n"
		. ( $telephone ? "Tél.    : $telephone\n" : '' ) . "Sujet   : $sujet\n\nMessage :\n$message";

	if ( defined( 'PA_RESEND_API_KEY' ) && PA_RESEND_API_KEY ) {
		$res = wp_remote_post( 'https://api.resend.com/emails', array(
			'timeout' => 15,
			'headers' => array( 'Authorization' => 'Bearer ' . PA_RESEND_API_KEY, 'Content-Type' => 'application/json' ),
			'body'    => wp_json_encode( array(
				'from'     => 'Paul Alves | Contact <' . $from . '>',
				'to'       => array( $to ),
				'reply_to' => $email,
				'subject'  => $subject,
				'html'     => $html,
				'text'     => $text,
			) ),
		) );
		$sent = ! is_wp_error( $res ) && wp_remote_retrieve_response_code( $res ) < 300;
		if ( ! $sent ) {
			error_log( '[pa] Resend ' . ( is_wp_error( $res ) ? $res->get_error_message() : wp_remote_retrieve_body( $res ) ) );
		}
	} else {
		$sent = wp_mail( $to, $subject, $html, array(
			'Content-Type: text/html; charset=UTF-8',
			'Reply-To: ' . $nom . ' <' . $email . '>',
		) );
	}

	if ( ! $sent ) {
		return new WP_REST_Response( array( 'error' => 'Erreur d\'envoi. Réessayez ou écrivez-moi directement à ' . PA_EMAIL . '.' ), 502 );
	}

	// Ajout dans Systeme.io (sans tag), non bloquant.
	$parts  = preg_split( '/\s+/', $nom );
	$fields = array( array( 'slug' => 'first_name', 'value' => $parts[0] ) );
	if ( count( $parts ) > 1 ) {
		$fields[] = array( 'slug' => 'surname', 'value' => implode( ' ', array_slice( $parts, 1 ) ) );
	}
	if ( $telephone ) {
		$fields[] = array( 'slug' => 'phone_number', 'value' => $telephone );
	}
	pa_systeme_io_add( array( 'email' => $email, 'fields' => $fields ) );

	return new WP_REST_Response( array( 'success' => true ), 200 );
}
