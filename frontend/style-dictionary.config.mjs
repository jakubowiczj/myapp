import StyleDictionary from 'style-dictionary';
import { register } from '@tokens-studio/sd-transforms';

// Rejestracja transformacji Tokens Studio (działa z style-dictionary v5 + sd-transforms v2)
register(StyleDictionary, {
  expandTypography: true,
  expandShadow: true,
  expandComposition: true,
  preserveRawValue: false
});

export default {
  // pojedynczy plik z tokenami
  source: ['tokens/tokens.json'],

  // gdzie mają trafić wygenerowane pliki
  platforms: {
    css: {
      transformGroup: 'tokens-studio',
      buildPath: 'styles/',
      files: [
        {
          destination: 'tokens.css',
          format: 'css/variables',
          options: {
            outputReferences: true,
            // nazwa selektora z CSS variables
            selector: ':root'
          }
        }
      ]
    },
    // (opcjonalnie) eksport do TS, jeśli chcesz używać tokenów w JS/TS
    js: {
      transformGroup: 'tokens-studio',
      buildPath: 'styles/',
      files: [
        {
          destination: 'tokens.ts',
          format: 'javascript/es6'
        }
      ]
    }
  }