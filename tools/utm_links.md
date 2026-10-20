# Tagged links

Each signup email's `source` field shows `utm_source / utm_medium / utm_campaign` from the visitor's first tagged landing (it falls back to the referrer, or "direct").

| Where | Link |
|---|---|
| Instagram bio | `https://spectra-render.com/?utm_source=instagram&utm_medium=bio&utm_campaign=beta` |
| Instagram story link | `https://spectra-render.com/?utm_source=instagram&utm_medium=story&utm_campaign=beta#beta` |
| Patreon | `https://spectra-render.com/?utm_source=patreon&utm_medium=post&utm_campaign=beta#beta` |
| YouTube description | `https://spectra-render.com/?utm_source=youtube&utm_medium=description&utm_campaign=beta` |
| Blender Artists / forums | `https://spectra-render.com/?utm_source=forum&utm_medium=post&utm_campaign=beta` |

Meta ads: use `https://spectra-render.com/#beta` as the destination, and paste this into the ad's **URL parameters** field so Meta fills in the names:

```
utm_source=meta&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}
```

New placement: copy a row and change `utm_source` and `utm_medium`. Keep them lowercase.
