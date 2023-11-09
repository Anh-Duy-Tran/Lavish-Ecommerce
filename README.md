# LAVISH ECOMERCIAL - FULL STACK NEXTJS version 13

Welcome to LAVISH, a web platform inspired by the Zara website's aesthetic and functionality. Built with the power of Nextjs version 13 and integrated with Contentful CMS, this app delivers a modern, user-centric shopping experience.

### Data Diagram

![Screenshot 2023-11-09 at 7 29 56](https://github.com/Anh-Duy-Tran/Lavish-Ecommerce/assets/113171462/4c374f26-a073-4048-86b1-dfa5df4fa791)

### Demo

- **Main functionalities**

https://github.com/Anh-Duy-Tran/Lavish-Ecommerce/assets/113171462/4716a0fe-8271-4754-9051-8933ef736035

- **Responsiveness**

https://github.com/Anh-Duy-Tran/Lavish-Ecommerce/assets/113171462/79590a03-2c8b-4f60-8bb5-ce04791f00e0

- **Ease of Content Management**

https://github.com/Anh-Duy-Tran/Lavish-Ecommerce/assets/113171462/7c237cc0-b8b7-4f4b-ac8d-be0a8f3d8d75

### Main Features

- **Data replicated from Zara API:** Meticulously crafted self-defined data schema to capture Zara product data structure.

- **Efficient Data Rendering**: For each product item in the main page, this app employs a lazy rendering technique (only fetch the first 2 images in the slider, fetch the rest only if the user interact with it). This significantly reduces latency, ensuring a swift browsing experience even with a large amount of product images and details.

- **View Switcher and Dark Mode:** Customize browsing experience with view and theme switcher, allowing you to toggle between different display layouts (the dark mode sync between tabs).

- **Image Slider:** A self-implemented, user-friendly image slider inspired by the Zara website ensures seamless navigation through the app product's image previews and main page.

- **Product Filters:** Our product page offers advanced filtering options. Users can easily filter out products based on their fundamental property, streamlining the shopping experience.

- **Contentful CMS:** A powerful content management system lets you manage your site's content effortlessly. It's act as admin content panel for a smooth administrative experience on a rich UI system.

- **User Authentication:** With dedicated login and registration system, users are assured a secure experience with cart and favourite item saving functionality.

- **Bilingual Languages:** LAVISH support two languages: English and Vietnamese through internationalization of content in the CMS

## Tech Stack

**Client:** React (Next.js), Zustand, TailwindCSS.

**Server:** Next.js (Node), Contentful Headless CMS.

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.
