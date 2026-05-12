import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14
import QtQuick.Window 2.14

ApplicationWindow {
    id: root
    visible: true
    width: Math.min(Screen.width, 480)
    height: Math.min(Screen.height, 900)
    title: "CubAutosFinder"
    color: bgPrimary

    // Colors
    property color bgPrimary: "#0d0d0d"
    property color bgSecondary: "#161616"
    property color bgCard: "#1a1a1a"
    property color bgElevated: "#202020"
    property color goldPrimary: "#d4af37"
    property color goldLight: "#f4cf57"
    property color orangeWarm: "#e85d04"
    property color textPrimary: "#f5f5f5"
    property color textSecondary: "#888888"
    property color borderSubtle: "#333333"

    property bool isLoading: apiClient.loading
    property int filterMaxAds: 30
    property bool filtersOpen: false
    property int selectedIndex: -1

    readonly property real scaleFactor: Math.min(width / 400, 1.2)

    Component.onCompleted: {
        apiClient.search("", 30, 0, 0, "", "")
    }

    // Stack for navigation
    StackView {
        id: stackView
        anchors.fill: parent
        initialItem: mainView
    }

    // Main View
    Component {
        id: mainView

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            // Header
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 60 * scaleFactor
                color: "#1a1a1a"

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 16 * scaleFactor
                    anchors.rightMargin: 16 * scaleFactor

                    ColumnLayout {
                        spacing: 2
                        Label {
                            text: "CubAutos"
                            font.pixelSize: 18 * scaleFactor
                            font.bold: true
                            color: goldPrimary
                        }
                        Label {
                            text: "Vehículos Eléctricos"
                            font.pixelSize: 10 * scaleFactor
                            color: textSecondary
                        }
                    }

                    Item { Layout.fillWidth: true }

                    Rectangle {
                        width: 32 * scaleFactor
                        height: 32 * scaleFactor
                        radius: width / 2
                        color: "transparent"
                        border.color: goldPrimary
                        border.width: 2 * scaleFactor
                        visible: isLoading
                        RotationAnimation on rotation {
                            from: 0; to: 360; duration: 1000; loops: Animation.Infinite
                        }
                    }

                    Text {
                        text: "✓"
                        font.pixelSize: 18 * scaleFactor
                        color: goldPrimary
                        visible: !isLoading
                    }
                }
            }

            // Status bar
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 32 * scaleFactor
                color: bgSecondary

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 12 * scaleFactor

                    Text {
                        text: apiClient.status
                        font.pixelSize: 11 * scaleFactor
                        color: isLoading ? goldPrimary : textSecondary
                    }

                    Item { Layout.fillWidth: true }

                    Text {
                        text: vehicleModel.count() + " resultados"
                        font.pixelSize: 11 * scaleFactor
                        color: goldPrimary
                        visible: vehicleModel.count() > 0
                    }
                }
            }

            // Filters Section
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: filtersOpen ? 220 * scaleFactor : 48 * scaleFactor
                color: bgSecondary
                clip: true

                Behavior on Layout.preferredHeight {
                    NumberAnimation { duration: 300; easing.type: Easing.InOutCubic }
                }

                ColumnLayout {
                    anchors.fill: parent

                    // Toggle Header
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 48 * scaleFactor
                        color: "transparent"

                        Rectangle {
                            width: parent.width
                            height: 1
                            color: borderSubtle
                            anchors.bottom: parent.bottom
                        }

                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 16 * scaleFactor

                            Label {
                                text: "Filtros"
                                font.pixelSize: 14 * scaleFactor
                                font.bold: true
                                color: goldPrimary
                            }

                            Item { Layout.fillWidth: true }

                            Text {
                                text: filtersOpen ? "▲" : "▼"
                                font.pixelSize: 12 * scaleFactor
                                color: textSecondary
                            }
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: filtersOpen = !filtersOpen
                        }
                    }

                    // Filters Panel
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        color: "transparent"
                        visible: filtersOpen

                        ColumnLayout {
                            anchors.centerIn: parent
                            width: parent.width * 0.9
                            spacing: 14 * scaleFactor

                            RowLayout {
                                spacing: 12 * scaleFactor
                                Layout.fillWidth: true

                                ColumnLayout {
                                    Layout.fillWidth: true
                                    Label {
                                        text: "Precio Min"
                                        font.pixelSize: 10 * scaleFactor
                                        color: textSecondary
                                    }
                                    TextField {
                                        id: txtMinPrice
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: 38 * scaleFactor
                                        font.pixelSize: 13 * scaleFactor
                                        placeholderText: "0"
                                        background: Rectangle { color: bgCard; radius: 8; border.width: 1; border.color: borderSubtle }
                                    }
                                }

                                ColumnLayout {
                                    Layout.fillWidth: true
                                    Label {
                                        text: "Precio Max"
                                        font.pixelSize: 10 * scaleFactor
                                        color: textSecondary
                                    }
                                    TextField {
                                        id: txtMaxPrice
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: 38 * scaleFactor
                                        font.pixelSize: 13 * scaleFactor
                                        placeholderText: "50000"
                                        background: Rectangle { color: bgCard; radius: 8; border.width: 1; border.color: borderSubtle }
                                    }
                                }
                            }

                            ColumnLayout {
                                Layout.fillWidth: true
                                Label {
                                    text: "Marca"
                                    font.pixelSize: 10 * scaleFactor
                                    color: textSecondary
                                }
                                ComboBox {
                                    id: cmbBrand
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 38 * scaleFactor
                                    font.pixelSize: 13 * scaleFactor
                                    model: ["Todas", "BYD", "Tesla", "Nissan", "BMW", "Chevrolet"]
                                    background: Rectangle { color: bgCard; radius: 8; border.width: 1; border.color: borderSubtle }
                                }
                            }

                            Button {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 44 * scaleFactor
                                background: Rectangle {
                                    color: goldPrimary
                                    radius: 10
                                }
                                contentItem: Text {
                                    text: "BUSCAR"
                                    color: "#0d0d0d"
                                    font.bold: true
                                    font.pixelSize: 14 * scaleFactor
                                    horizontalAlignment: Text.AlignHCenter
                                }
                                onClicked: {
                                    vehicleModel.clear()
                                    var minP = parseFloat(txtMinPrice.text) || 0
                                    var maxP = parseFloat(txtMaxPrice.text) || 0
                                    var brand = cmbBrand.currentText || ""
                                    if (brand === "Todas") brand = ""
                                    apiClient.search("", filterMaxAds, minP, maxP, brand, "")
                                }
                            }
                        }
                    }
                }
            }

            // Content
            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Rectangle {
                    anchors.centerIn: parent
                    width: parent.width
                    height: 150 * scaleFactor
                    color: "transparent"
                    visible: isLoading

                    ColumnLayout {
                        anchors.centerIn: parent
                        spacing: 12 * scaleFactor

                        Rectangle {
                            width: 50 * scaleFactor
                            height: 50 * scaleFactor
                            radius: width / 2
                            color: "transparent"
                            border.color: goldPrimary
                            border.width: 3 * scaleFactor
                            RotationAnimation on rotation {
                                from: 0; to: 360; duration: 1200; loops: Animation.Infinite
                            }
                        }

                        Text {
                            text: "Obteniendo datos..."
                            font.pixelSize: 13 * scaleFactor
                            color: goldPrimary
                        }
                    }
                }

                ListView {
                    id: listView
                    anchors.fill: parent
                    model: vehicleModel
                    spacing: 10 * scaleFactor
                    visible: !isLoading
                    clip: true
                    leftMargin: 12 * scaleFactor
                    rightMargin: 12 * scaleFactor
                    topMargin: 8 * scaleFactor
                    bottomMargin: 8 * scaleFactor

                    delegate: Rectangle {
                        width: listView.width - 24 * scaleFactor
                        height: 150 * scaleFactor
                        color: bgCard
                        radius: 12 * scaleFactor
                        border.width: selectedIndex === index ? 2 : 1
                        border.color: selectedIndex === index ? goldPrimary : borderSubtle

                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 10 * scaleFactor
                            spacing: 10 * scaleFactor

                            Rectangle {
                                Layout.preferredWidth: 100 * scaleFactor
                                Layout.fillHeight: true
                                radius: 8 * scaleFactor
                                color: bgElevated

                                Image {
                                    anchors.fill: parent
                                    anchors.margins: 3 * scaleFactor
                                    fillMode: Image.PreserveAspectCrop
                                    source: imageUrl || ""
                                }

                                Rectangle {
                                    anchors.top: parent.top
                                    anchors.left: parent.left
                                    anchors.margins: 5 * scaleFactor
                                    height: 18 * scaleFactor
                                    width: 50 * scaleFactor
                                    color: bgElevated
                                    radius: 4 * scaleFactor
                                    border.width: 1
                                    border.color: borderSubtle

                                    Text {
                                        anchors.centerIn: parent
                                        text: sourceLabel || source || ""
                                        color: goldPrimary
                                        font.pixelSize: 8 * scaleFactor
                                        font.bold: true
                                    }
                                }
                            }

                            ColumnLayout {
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                spacing: 4 * scaleFactor

                                Text {
                                    text: title || "Sin título"
                                    font.pixelSize: 12 * scaleFactor
                                    font.bold: true
                                    color: textPrimary
                                    wrapMode: Text.WordWrap
                                    maximumLineCount: 2
                                    Layout.fillWidth: true
                                }

                                Text {
                                    text: price > 0 ? "$" + price : "Consultar"
                                    font.pixelSize: 16 * scaleFactor
                                    font.bold: true
                                    color: goldPrimary
                                }

                                RowLayout {
                                    spacing: 4 * scaleFactor
                                    Text { text: "📍"; font.pixelSize: 9 * scaleFactor }
                                    Text {
                                        text: province || "Cuba"
                                        color: textSecondary
                                        font.pixelSize: 10 * scaleFactor
                                    }
                                }

                                Text {
                                    text: autonomiaKm > 0 ? "🔋 " + autonomiaKm + " km" : ""
                                    color: orangeWarm
                                    font.pixelSize: 10 * scaleFactor
                                    visible: autonomiaKm > 0
                                }

                                Item { Layout.fillHeight: true }
                            }
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                selectedIndex = index
                                stackView.push(detailView)
                            }
                        }
                    }
                }

                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: 10 * scaleFactor
                    visible: !isLoading && vehicleModel.count() === 0

                    Text { text: "🔍"; font.pixelSize: 36 * scaleFactor; horizontalAlignment: Text.AlignHCenter }
                    Text { text: "Sin resultados"; font.pixelSize: 15 * scaleFactor; font.bold: true; color: textPrimary }
                    Text { text: "Intenta con otros filtros"; font.pixelSize: 12 * scaleFactor; color: textSecondary }
                }
            }
        }
    }

    // Detail View - Clean & Organized
    Component {
        id: detailView

        Rectangle {
            color: bgPrimary

            ColumnLayout {
                anchors.fill: parent
                spacing: 0

                // Header with back button
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 56 * scaleFactor
                    color: "#1a1a1a"

                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 12 * scaleFactor

                        Button {
                            background: Rectangle { color: "transparent" }
                            contentItem: Text {
                                text: "← Volver"
                                color: goldPrimary
                                font.pixelSize: 14 * scaleFactor
                            }
                            onClicked: stackView.pop()
                        }

                        Item { Layout.fillWidth: true }

                        Text {
                            text: "Detalle"
                            font.pixelSize: 16 * scaleFactor
                            font.bold: true
                            color: textPrimary
                        }

                        Item { Layout.fillWidth: true }
                    }
                }

                // Scrollable Content
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true

                    ColumnLayout {
                        width: parent.width
                        spacing: 12 * scaleFactor
                        anchors.margins: 14 * scaleFactor

                        // Image
                        Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 160 * scaleFactor
                            color: bgCard
                            radius: 10 * scaleFactor
                            clip: true

                            Image {
                                anchors.fill: parent
                                fillMode: Image.PreserveAspectCrop
                                source: vehicleModel.get(selectedIndex).imageUrl || ""
                            }
                        }

                        // Title Card
                        Rectangle {
                            Layout.fillWidth: true
                            color: bgCard
                            radius: 10 * scaleFactor

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 14 * scaleFactor
                                spacing: 6 * scaleFactor

                                Text {
                                    text: vehicleModel.get(selectedIndex).title || "Sin título"
                                    font.pixelSize: 15 * scaleFactor
                                    font.bold: true
                                    color: textPrimary
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                }

                                Text {
                                    text: vehicleModel.get(selectedIndex).price > 0 
                                        ? "$" + vehicleModel.get(selectedIndex).price + " " + (vehicleModel.get(selectedIndex).currency || "USD")
                                        : "Consultar precio"
                                    font.pixelSize: 22 * scaleFactor
                                    font.bold: true
                                    color: goldPrimary
                                }

                                RowLayout {
                                    spacing: 6 * scaleFactor
                                    Text { text: "📍"; font.pixelSize: 11 * scaleFactor }
                                    Text {
                                        text: (vehicleModel.get(selectedIndex).province || "Cuba") + 
                                              (vehicleModel.get(selectedIndex).municipality ? ", " + vehicleModel.get(selectedIndex).municipality : "")
                                        color: textSecondary
                                        font.pixelSize: 11 * scaleFactor
                                    }
                                }

                                Text {
                                    text: "Fuente: " + (vehicleModel.get(selectedIndex).sourceLabel || vehicleModel.get(selectedIndex).source || "")
                                    color: goldPrimary
                                    font.pixelSize: 10 * scaleFactor
                                }
                            }
                        }

                        // Specs Card
                        Rectangle {
                            Layout.fillWidth: true
                            color: bgCard
                            radius: 10 * scaleFactor

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 14 * scaleFactor
                                spacing: 10 * scaleFactor

                                Text {
                                    text: "Especificaciones"
                                    font.pixelSize: 13 * scaleFactor
                                    font.bold: true
                                    color: goldPrimary
                                }

                                // Specs Grid - 2 columns
                                GridLayout {
                                    columns: 2
                                    columnSpacing: 10 * scaleFactor
                                    rowSpacing: 10 * scaleFactor
                                    Layout.fillWidth: true

                                    // Autonomy
                                    Rectangle {
                                        color: bgElevated
                                        radius: 8 * scaleFactor
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: 70 * scaleFactor

                                        ColumnLayout {
                                            anchors.centerIn: parent
                                            spacing: 4 * scaleFactor
                                            Text { text: "🔋"; font.pixelSize: 20 * scaleFactor; horizontalAlignment: Text.AlignHCenter }
                                            Text { text: "Autonomía"; font.pixelSize: 10 * scaleFactor; color: textSecondary; horizontalAlignment: Text.AlignHCenter }
                                            Text {
                                                text: vehicleModel.get(selectedIndex).autonomiaKm > 0 
                                                    ? vehicleModel.get(selectedIndex).autonomiaKm + " km" : "N/A"
                                                font.pixelSize: 13 * scaleFactor; font.bold: true; color: textPrimary; horizontalAlignment: Text.AlignHCenter
                                            }
                                        }
                                    }

                                    // Battery
                                    Rectangle {
                                        color: bgElevated
                                        radius: 8 * scaleFactor
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: 70 * scaleFactor

                                        ColumnLayout {
                                            anchors.centerIn: parent
                                            spacing: 4 * scaleFactor
                                            Text { text: "⚡"; font.pixelSize: 20 * scaleFactor; horizontalAlignment: Text.AlignHCenter }
                                            Text { text: "Batería"; font.pixelSize: 10 * scaleFactor; color: textSecondary; horizontalAlignment: Text.AlignHCenter }
                                            Text {
                                                text: vehicleModel.get(selectedIndex).batteryKwh > 0
                                                    ? vehicleModel.get(selectedIndex).batteryKwh + " kWh" : "N/A"
                                                font.pixelSize: 13 * scaleFactor; font.bold: true; color: textPrimary; horizontalAlignment: Text.AlignHCenter
                                            }
                                        }
                                    }

                                    // Charging
                                    Rectangle {
                                        color: bgElevated
                                        radius: 8 * scaleFactor
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: 70 * scaleFactor

                                        ColumnLayout {
                                            anchors.centerIn: parent
                                            spacing: 4 * scaleFactor
                                            Text { text: "⏱"; font.pixelSize: 20 * scaleFactor; horizontalAlignment: Text.AlignHCenter }
                                            Text { text: "Carga 10-80%"; font.pixelSize: 10 * scaleFactor; color: textSecondary; horizontalAlignment: Text.AlignHCenter }
                                            Text {
                                                text: vehicleModel.get(selectedIndex).chargingTime || "N/A"
                                                font.pixelSize: 13 * scaleFactor; font.bold: true; color: textPrimary; horizontalAlignment: Text.AlignHCenter
                                            }
                                        }
                                    }

                                    // Model
                                    Rectangle {
                                        color: bgElevated
                                        radius: 8 * scaleFactor
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: 70 * scaleFactor

                                        ColumnLayout {
                                            anchors.centerIn: parent
                                            spacing: 4 * scaleFactor
                                            Text { text: "🚗"; font.pixelSize: 20 * scaleFactor; horizontalAlignment: Text.AlignHCenter }
                                            Text { text: "Modelo"; font.pixelSize: 10 * scaleFactor; color: textSecondary; horizontalAlignment: Text.AlignHCenter }
                                            Text {
                                                text: vehicleModel.get(selectedIndex).modelo || "N/A"
                                                font.pixelSize: 13 * scaleFactor; font.bold: true; color: textPrimary; horizontalAlignment: Text.AlignHCenter
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // Contact Card
                        Rectangle {
                            Layout.fillWidth: true
                            color: bgCard
                            radius: 10 * scaleFactor

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 14 * scaleFactor
                                spacing: 10 * scaleFactor

                                Text {
                                    text: "Contacto"
                                    font.pixelSize: 13 * scaleFactor
                                    font.bold: true
                                    color: goldPrimary
                                }

                                ColumnLayout {
                                    spacing: 10 * scaleFactor
                                    Layout.fillWidth: true

                                    // Name
                                    RowLayout {
                                        spacing: 10 * scaleFactor
                                        Text { text: "👤"; font.pixelSize: 14 * scaleFactor }
                                        Text {
                                            text: vehicleModel.get(selectedIndex).contactName || "No disponible"
                                            color: textPrimary
                                            font.pixelSize: 13 * scaleFactor
                                            Layout.fillWidth: true
                                        }
                                    }

                                    // Phone
                                    RowLayout {
                                        spacing: 10 * scaleFactor
                                        Text { text: "📞"; font.pixelSize: 14 * scaleFactor }
                                        Text {
                                            text: vehicleModel.get(selectedIndex).contactPhone || "No disponible"
                                            color: textPrimary
                                            font.pixelSize: 13 * scaleFactor
                                            Layout.fillWidth: true
                                        }
                                    }

                                    // WhatsApp
                                    RowLayout {
                                        spacing: 10 * scaleFactor
                                        Text { text: "💬"; font.pixelSize: 14 * scaleFactor }
                                        Text {
                                            text: vehicleModel.get(selectedIndex).contactWhatsapp || "No disponible"
                                            color: orangeWarm
                                            font.pixelSize: 13 * scaleFactor
                                            Layout.fillWidth: true
                                        }
                                    }
                                }
                            }
                        }

                        // Description Card
                        Rectangle {
                            Layout.fillWidth: true
                            color: bgCard
                            radius: 10 * scaleFactor

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 14 * scaleFactor
                                spacing: 8 * scaleFactor

                                Text {
                                    text: "Descripción"
                                    font.pixelSize: 13 * scaleFactor
                                    font.bold: true
                                    color: goldPrimary
                                }

                                Text {
                                    text: vehicleModel.get(selectedIndex).description || "Sin descripción disponible."
                                    color: textSecondary
                                    font.pixelSize: 12 * scaleFactor
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                }
                            }
                        }

                        // Link Button
                        Button {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 48 * scaleFactor
                            background: Rectangle {
                                color: goldPrimary
                                radius: 10
                            }
                            contentItem: Text {
                                text: "Ver Anuncio Original"
                                color: "#0d0d0d"
                                font.bold: true
                                font.pixelSize: 14 * scaleFactor
                                horizontalAlignment: Text.AlignHCenter
                            }
                            onClicked: {
                                Qt.openUrlExternally(vehicleModel.get(selectedIndex).url || "")
                            }
                        }

                        Item { Layout.preferredHeight: 20 * scaleFactor }
                    }
                }
            }
        }
    }
}