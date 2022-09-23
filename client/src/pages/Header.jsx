export default function Header(prop) {

    return (
        <>
            <nav className="px- px-2 sm:px-4 py-2.5 bg-gray-50 border-gray-200 dark:bg-gray-800 dark:border-gray-700 text-gray-900 text-sm rounded border dark:text-white">
                <div className="container mx-auto flex flex-wrap items-center justify-between">
                    <div className="flex">
                        <span className="self-center text-lg font-semibold whitespace-nowrap text-gray-900 dark:text-white">
                            Chat Room
                        </span>
                    </div>
                    <div className="flex md:order-2">
                    </div>
                    <div className="flex  top-0 right-0">
                        <div>
                            <span>User : </span>
                            <strong>{prop.prop}</strong>
                        </div>
                    </div>
                </div>
            </nav>

        </>
    );
}