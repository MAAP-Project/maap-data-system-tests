#!/usr/bin/env ruby

require 'openssl'
require 'jwt'  # https://rubygems.org/gems/jwt

puts JWT.encode(
  {
    # issued at time, 60 seconds in the past to allow for clock drift
    iat: Time.now.to_i - 60,
    # JWT expiration time (10 minute maximum)
    exp: Time.now.to_i + (10 * 60),
    # GitHub App's identifier
    iss: "153910"
  }, 
  OpenSSL::PKey::RSA.new(
    File.read("maap-system-tests.2021-11-23.private-key.pem")
  ), 
  "RS256"
)
